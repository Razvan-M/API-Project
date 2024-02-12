FROM python:3.9.18

RUN pip install poetry==1.6.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /usr/src/app

RUN touch README.md

COPY poetry.lock pyproject.toml ./

RUN poetry install && rm -rf $POETRY_CACHE_DIR

COPY . .

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]