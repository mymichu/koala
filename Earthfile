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
    RUN poetry run isort . --check
    RUN poetry run pylint koala --reports=y
    RUN poetry run black . --check
    RUN poetry run flake8 koala
    RUN poetry run mypy .
    RUN poetry run bandit -r koala
    
build:
    FROM +check
    RUN poetry build

test:
    FROM +install
    ENV IMMUDB_HOST="localhost"
    COPY .devcontainer .devcontainer
    WITH DOCKER --compose .devcontainer/docker-compose.yml \
        --service database
        RUN poetry run pytest --md-report --md-report-verbose=1
    END
