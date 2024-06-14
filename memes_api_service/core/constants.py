PREFIX_POSTGRES = 'POSTGRES_'
PREFIX_SQLITE = 'SQLITE_'
PREFIX_APP = 'APP_'

SQLITE_URL = '{driver}:///./{db_name}'
PG_URL = '{driver}://{user}:{password}@{host}:{port}/{db_name}'

ENCODING = 'utf-8'


MEMES_PREFIX = '/memes'
MEMES_TAG = 'Мемы'

USER_PREFIX = '/users'
USER_TAG = 'Пользователи'

SIGNUP_PREFIX = '/auth'
SIGNUP_TAG = 'Регистрация'

AUTH_PREFIX = '/auth/jwt'
AUTH_TAG = 'Аутентификация'


AUTH_BACKEND_NAME = 'jwt'
AUTH_TOKEN_URL = 'auth/jwt/login'
JWT_LIFETIME = 3600


DEFAULT_PAGE = 1
DEFAULT_LIMIT_PER_PAGE = 5
MIN_STR_LENGTH = 1
MIN_PASSWORD_LENGTH = 8
MAX_TEXT_LENGTH = 1024

PASSWORD_LENGTH_ERROR = 'Длина пароля должна быть не менее 8 символов'
PASSWORD_SHOULDNT_CONTAINS_EMAIL = (
    'Пароль не должен состоять из электронного адреса'
)


FIELD_TEXT_CANNOT_BE_EMPTY = 'Поле text не должно быть пустым'
FIELD_TEXT_MAX_LENGTH_ERROR = (
    'Длина поля text не должна превышать 1024 символов'
)

FIELD_IMAGE_CANNOT_BE_EMPTY = 'Поле image не должно быть пустым'
FIELD_IMAGE_URL_LENGTH_ERROR = (
    'Длина поля image_url не должна превышать 2048 символов'
)

MEME_NOT_FOUND = 'Мем не найден'
CANNOT_EDIT_OR_DELETE_FOR_NOT_OWNER = 'Нельзя изменить или удалить чужой мем'

NO_CONNECTION = 'Нет соединения с сервером'
