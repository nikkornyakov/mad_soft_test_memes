from http import HTTPStatus

from fastapi.exceptions import HTTPException

from core.constants import NO_CONNECTION

no_connection_exception = HTTPException(
    detail=NO_CONNECTION, status_code=HTTPStatus.SERVICE_UNAVAILABLE
)
