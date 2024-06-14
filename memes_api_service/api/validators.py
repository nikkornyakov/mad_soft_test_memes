from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import (
    CANNOT_EDIT_OR_DELETE_FOR_NOT_OWNER,
    FIELD_TEXT_CANNOT_BE_EMPTY,
    FIELD_TEXT_MAX_LENGTH_ERROR,
    MAX_TEXT_LENGTH,
    MEME_NOT_FOUND,
    MIN_STR_LENGTH,
)
from crud.memes import memes_crud
from models import Meme, User


async def check_meme_exists(meme_id: int, session: AsyncSession) -> None:
    """
    Функция для проверки наличия мема в базе данных.

    Принимает параметры:
        - meme_id - id мема;
        - session - асинхронная сессия для работы с базой данных.

    Возвращает None в случае успешной проверки или HTTPException
     с информацией о том, что мем не найден в базе данных.
    """
    if not await memes_crud.get(meme_id, session):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=MEME_NOT_FOUND
        )


async def check_meme_before_edit_and_delete(
    meme_id: int, user: User, session: AsyncSession
) -> Meme:
    """
    Функция для проверки наличия мема в базе данных.

    Принимает параметры:
        - meme_id - id мема;
        - user - текущий пользователь;
        - session - асинхронная сессия для работы с базой данных.

    Возвращает None в случае успешной проверки или HTTPException
    с информацией о том, что мем не найден в базе данных
    или нет соответствующих прав.
    """
    await check_meme_exists(meme_id, session)
    meme = await memes_crud.get(meme_id, session)
    if not user.is_superuser and meme.user_id != user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=CANNOT_EDIT_OR_DELETE_FOR_NOT_OWNER,
        )


def validate_text(text):
    """
    Функция для валидации текста мема.

    Принимает параметры:
        - text - текст мема.

    Возвращает None в случае успешной проверки или HTTPException
     с информацией об ошибке.
    """
    if len(text) < MIN_STR_LENGTH:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=FIELD_TEXT_CANNOT_BE_EMPTY,
        )
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=FIELD_TEXT_MAX_LENGTH_ERROR,
        )
