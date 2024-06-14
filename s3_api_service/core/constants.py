PREFIX_POSTGRES = 'POSTGRES_'
PREFIX_SQLITE = 'SQLITE_'
PREFIX_APP = 'APP_'
PREFIX_S3 = 'S3_'

SQLITE_URL = '{driver}:///./{db_name}'
PG_URL = '{driver}://{user}:{password}@{host}:{port}/{db_name}'

S3_URL = '{}/{}'
S3_FILE_URL = f'{S3_URL}/{{}}'

NEW_FILENAME = '{}({}).{}'

ENCODING = 'utf-8'

USER_PREFIX = '/users'
USER_TAG = 'Пользователи'

AUTH_PREFIX = '/auth/jwt'
AUTH_TAG = 'Аутентификация'

MEDIA_TAG = 'Управление медиа'

AUTH_BACKEND_NAME = 'jwt'
AUTH_TOKEN_URL = 'auth/jwt/login'
JWT_LIFETIME = 3600

NOT_FOUND_FILE = 'Файл в хранилище не найден'
NO_CONNECTION = 'Не удалось подключиться к хранилищу'
SUCCESSFUL_DELETE = 'Файл {} успешно удален из хранилища'

NOT_FOUND_CODE = '404'
