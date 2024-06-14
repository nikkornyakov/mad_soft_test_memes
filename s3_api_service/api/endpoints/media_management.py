from http import HTTPStatus

from botocore.exceptions import EndpointConnectionError
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse

from api.exceptions import no_connection_exception
from api.utils import get_image_or_exception, get_new_filename
from api.validators import check_file_exists
from core.config import app_config
from core.constants import S3_FILE_URL, SUCCESSFUL_DELETE
from core.user import current_user_is_superuser

router = APIRouter()


@router.get('/{filename}', dependencies=[Depends(current_user_is_superuser)])
async def get_file_by_filename(filename: str):
    """
    Функция для получения файла с изображением по его имени.

    Принимает параметры:
        - filename - имя файла.
    """
    bucket_name = (
        app_config.storage_client.create_bucket_and_or_get_bucket_name()
    )
    try:
        image = get_image_or_exception(bucket_name, filename)
        return JSONResponse(
            content=dict(
                filename=filename,
                content_type=image['ContentType'],
                created_at=str(image['LastModified']),
            )
        )
    except EndpointConnectionError:
        raise no_connection_exception


@router.delete(
    '/{filename}', dependencies=[Depends(current_user_is_superuser)]
)
async def delete_image_from_s3(filename: str):
    """
    Функция для удаления файла с изображением по его имени.

    Принимает параметры:
        - filename - имя файла.
    """
    bucket_name = (
        app_config.storage_client.create_bucket_and_or_get_bucket_name()
    )
    get_image_or_exception(bucket_name, filename)
    try:
        app_config.storage_client.get_client().delete_object(
            Bucket=bucket_name, Key=filename
        )
        return JSONResponse(
            content=dict(detail=SUCCESSFUL_DELETE.format(filename)),
            status_code=HTTPStatus.OK,
        )
    except EndpointConnectionError:
        raise no_connection_exception


@router.post('/upload')
async def upload_image_to_s3(image: UploadFile = File(...)):
    """
    Функция для загрузки файла с изображением в S3 хранилище.

    Принимает параметры:
        - image - файл с изображением.
    """
    bucket_name = (
        app_config.storage_client.create_bucket_and_or_get_bucket_name()
    )
    filename = image.filename
    try:
        if check_file_exists(bucket_name, filename):
            filename = get_new_filename(filename, bucket_name)
        app_config.storage_client.get_client().upload_fileobj(
            image.file,
            bucket_name,
            filename,
            ExtraArgs=dict(ContentType=image.content_type),
        )
        return JSONResponse(
            content=dict(
                image_url=S3_FILE_URL.format(
                    app_config.storage_client.url,
                    bucket_name,
                    filename,
                )
            )
        )
    except EndpointConnectionError:
        raise no_connection_exception
