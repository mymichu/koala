VERSION 0.6

build:
    FROM DOCKERFILE .devcontainer
    COPY backend /backend
    WORKDIR /backend
    RUN poetry config virtualenvs.in-project true && poetry update
    RUN poetry install
    RUN poetry run mypy
    RUN poetry build