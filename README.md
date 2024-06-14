# Тестовое задание на вакансию Python-разработчик в компанию Mad Soft
## Описание проекта
Проект состоит из нескольких сервисов:
- публичный API-сервис для управления коллекцией мемов с регистрацией пользователей;
- S3-совместимое хранилище для хранения файлов с изображениями мемов;
- приватный API-сервис для управления содержимым S3-совместимого хранилища.

## Стэк технологий
![](https://img.shields.io/badge/Python-white?logo=python&style=plastic)
![](https://img.shields.io/badge/FastAPI-white?logo=fastapi&style=plastic)
![](https://img.shields.io/badge/Pydantic-white?logo=pydantic&logoColor=black&style=plastic)
![](https://img.shields.io/badge/SQLAlchemy-white?logo=sqlalchemy&logoColor=black&style=plastic)
![](https://img.shields.io/badge/Alembic-white?logo=alembic&style=plastic)
![](https://img.shields.io/badge/Uvicorn-white?logo=uvicorn&style=plastic)
![](https://img.shields.io/badge/PostgreSQL-white?logo=postgresql&style=plastic)
![](https://img.shields.io/badge/AWS%20S3-white?logo=amazon-s3&style=plastic)
![](https://img.shields.io/badge/Docker-white?logo=docker&style=plastic)


## Инструкция по локальной сборке и локальному запуску
*Предполагается наличие на локальной машине установленного Docker*

**1.** Клонируйте репозиторий себе на машину командой в терминале:
  ```
  git clone https://github.com/nikkornyakov/test_test_test.git
  ```

**2.** В корневой директории проекта создайте файл .env и скопируйте в него данные из файла .env.example(рекомендуется) либо подставьте свои данные при необходимости

**3.** Запустите оркестрацию контейнеров при помощи следующей команды:
  ```
  docker compose -f docker-compose.local.yml up
  ```

**4.** Дождитесь запуска всех контейнеров. В случае успешного запуска в терминале должен быть похожий вывод:
  ```
  db_users   | 2024-06-14 12:51:21.428 UTC [1] LOG:  database system is ready to accept connections
  db_memes   | 2024-06-14 12:51:21.429 UTC [1] LOG:  database system is ready to accept connections
  s3_api     | INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
  s3_api     | INFO  [alembic.runtime.migration] Will assume transactional DDL.
  s3_api     | INFO  [alembic.runtime.migration] Running upgrade  -> 5791ed1b719f, Add user model.
  memes_api  | INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
  memes_api  | INFO  [alembic.runtime.migration] Will assume transactional DDL.
  memes_api  | INFO  [alembic.runtime.migration] Running upgrade  -> 4264a431e577, Add user and meme models.
  s3_api     | INFO:     Started server process [1]
  s3_api     | INFO:     Waiting for application startup.
  s3_api     | INFO:     Application startup complete.
  s3_api     | INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
  memes_api  | INFO:     Started server process [1]
  memes_api  | INFO:     Waiting for application startup.
  memes_api  | INFO:     Application startup complete.
  memes_api  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
  ```

**5.** Перейдите на сайт с документацией API-сервисов и ознакомьтесь с ней:
  - для API-сервиса управления коллекцией мемов: http://127.0.0.1:8000/docs
  - для API-сервиса управления S3-совместимым хранилищем: http://127.0.0.1:8080/docs

**6.** Попрактикуйтесь, отправляю различные запросы. При необходимости зарегистрируйте нового пользователя либо войдите в качестве суперпользователя, данные которого указаны в env-файле. 

## Автор

[Nikita Kornyakov](https://github.com/nikkornyakov)
