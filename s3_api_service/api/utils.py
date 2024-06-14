from http import HTTPStatus

from fastapi.exceptions import HTTPException

from api.validators import check_file_exists
from core.config import app_config
from core.constants import NEW_FILENAME, NOT_FOUND_FILE


def get_new_filename(filename, bucket_name):
    """
    Функция получения нового имени файла.

    Принимает параметры:
        - filename - имя файла;
        - bucket_name - имя бакета в S3 хранилище.

    Возвращает новое имя файла.
    """
    name, extension = filename.split('.')
    counter = 1
    new_filename = NEW_FILENAME.format(name, counter, extension)
    while check_file_exists(bucket_name, new_filename):
        counter += 1
        new_filename = NEW_FILENAME.format(name, counter, extension)
    return new_filename


def get_image_or_exception(bucket_name: str, filename: str):
    """
    Функция получения файла с изображением по имени.

    Принимает параметры:
        - bucket_name - имя бакета в S3 хранилище;
        - filename - имя файла с изображением.

    Возвращает искомый файл с изображением или исключение,
                                    если такого файла нет.
    """
    if not check_file_exists(bucket_name, filename):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND_FILE,
        )
    return app_config.storage_client.get_client().head_object(
        Bucket=app_config.storage_client.bucket_name, Key=filename
    )
