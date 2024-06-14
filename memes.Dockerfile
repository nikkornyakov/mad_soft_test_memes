FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /

RUN pip install --no-cache-dir poetry==1.8.2 && poetry config virtualenvs.create false && poetry install

COPY /memes_api_service .env entrypoint.sh /app/

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]