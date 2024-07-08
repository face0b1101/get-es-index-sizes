# The Builder Image, Used to Build the Virtual Environment
FROM python:3.11-buster as builder

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

# The Runtime Image, simply runs the code within the created virtual environment
FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="$PYTHONPATH:/"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Create /output directory
RUN mkdir /output

COPY src/get_es_index_sizes ./get_es_index_sizes

CMD ["python", "-m", "get_es_index_sizes.main"]
