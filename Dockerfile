FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

COPY src/ /app/src/

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi