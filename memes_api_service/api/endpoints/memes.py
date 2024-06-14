from http import HTTPStatus

import requests
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.validators import (
    check_meme_before_edit_and_delete,
    check_meme_exists,
    validate_text,
)
from core.config import app_config
from core.constants import DEFAULT_LIMIT_PER_PAGE, DEFAULT_PAGE, NO_CONNECTION
from core.db import get_async_session
from core.user import current_user
from crud.memes import memes_crud
from models import User
from schemas.memes import MemeCreateUpdate, MemeRead

router = APIRouter()


@router.get('/', response_model=list[MemeRead])
async def get_all_memes(
    page: int = Query(DEFAULT_PAGE),
    limit: int = Query(DEFAULT_LIMIT_PER_PAGE),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Функция для получения списка всех мемов с пагинацией.

    Принимает параметры:
        - page: int - номер страницы(по умолчанию - 1);
        - limit: int - количество мемов на странице(по умолчанию - 5);
        - session - асинхронная сессия для выполнения запросов к базе данных.
    """
    left_index = (page - 1) * limit
    return (await memes_crud.get_all(session))[left_index : left_index + limit]


@router.get('/{id}', response_model=MemeRead)
async def get_meme(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Функция для получения конкретного мемов по его id.

    Принимает параметры:
        - id: int - id мема;
        - session - асинхронная сессия для выполнения запросов к базе данных.
    """
    await check_meme_exists(id, session)
    return await memes_crud.get(id, session)


@router.post(
    '/',
    response_model=MemeRead,
)
async def post_meme(
    text: str = Form(...),
    image: UploadFile = File(...),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Функция добавления мема в базу данных.
    Необходима авторизация.

    Принимает параметры:
        - text: str - текст мема длиной не более 1024 символов;
        - image - файл с изображением мема;
        - user - текущий пользователь;
        - session - асинхронная сессия для выполнения запросов к базе данных.
    """
    validate_text(text)
    try:
        response = requests.post(
            url=app_config.app.s3_api_upload_url,
            files=dict(image=(image.filename, image.file, image.content_type)),
        )
    except requests.exceptions.ConnectionError:
        return JSONResponse(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            content=dict(detail=NO_CONNECTION),
        )
    return await memes_crud.create(
        MemeCreateUpdate(
            image_url=response.json()['image_url'], text=text, user_id=user.id
        ),
        session,
    )


@router.put(
    '/{id}',
    response_model=MemeRead,
)
async def full_update_meme(
    id: int,
    text: str = Form(...),
    image: UploadFile = File(...),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Функция для полного изменения мема по его id.
    Необходима авторизация.

    Принимает параметры:
        - id: int - id мема;
        - text: str - текст мема длиной не более 1024 символов;
        - image - файл с изображением мема;
        - user - текущий пользователь;
        - session - асинхронная сессия для выполнения запросов к базе данных.
    """
    await check_meme_before_edit_and_delete(id, user, session)
    validate_text(text)
    try:
        response = requests.post(
            url=app_config.app.s3_api_upload_url,
            files=dict(image=(image.filename, image.file, image.content_type)),
        )
    except requests.exceptions.ConnectionError:
        return JSONResponse(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            content=dict(detail=NO_CONNECTION),
        )
    return await memes_crud.update(
        await memes_crud.get(id, session),
        MemeCreateUpdate(
            image_url=response.json()['image_url'], text=text, user_id=user.id
        ),
        session,
    )


@router.delete(
    '/{id}',
    response_model=MemeRead,
)
async def delete_meme(
    id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Функция удаления мема из базы данных.
    Необходима авторизация.

    Принимает параметры:
        - id: int - id мема;
        - user - текущий пользователь;
        - session - асинхронная сессия для выполнения запросов к базе данных.
    """
    await check_meme_before_edit_and_delete(id, user, session)
    return await memes_crud.remove(await memes_crud.get(id, session), session)
