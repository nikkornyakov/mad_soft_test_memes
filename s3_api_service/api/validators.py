from botocore.exceptions import ClientError

from core.config import app_config
from core.constants import NOT_FOUND_CODE


def check_file_exists(bucket, filename) -> bool:
    """
    Функция проверки наличия файла в S3 хранилище.

    Принимает параметры:
        - bucket - имя бакета в S3 хранилище;
        - filename - имя искомого файла.

    Возвращает True в случае успешной проверки или False.
    """
    try:
        app_config.storage_client.get_client().head_object(
            Bucket=bucket, Key=filename
        )
        return True
    except ClientError as error:
        if error.response['Error']['Code'] == NOT_FOUND_CODE:
            return False
