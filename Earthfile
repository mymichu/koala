VERSION 0.6



docker:
    FROM fnndsc/python-poetry
    COPY backend ./backend
    WORKDIR ./backend
    SAVE IMAGE backend:latest

install:
    FROM +docker
    RUN poetry update
    RUN poetry install

check:
    FROM +install
#    RUN poetry run isort . --check
    RUN poetry run mypy .

build:
    FROM +check
    RUN poetry build

test:
    FROM +install
    ENV IMMUDB_HOST="localhost"
    COPY .devcontainer .devcontainer
    WITH DOCKER --compose .devcontainer/docker-compose.yml \
        --service database
        RUN poetry run pytest
    END
