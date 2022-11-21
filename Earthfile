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
    SAVE ARTIFACT dist AS LOCAL dist

test:
    FROM +install
    ENV IMMUDB_HOST="localhost"
    COPY .devcontainer .devcontainer
    WITH DOCKER --compose .devcontainer/docker-compose.yml \
        --service database
    RUN poetry run pytest --md-report --md-report-verbose=1
    END

docker-app:
    FROM python:3.10.5-buster
    COPY +build/dist dist
    RUN pip install dist/*.whl
    ENTRYPOINT python3 -m koala 
    SAVE IMAGE ghcr.io/mymichu/koala:latest

sys-test:
    FROM earthly/dind:alpine
    RUN apk update && apk add --no-cache \
        curl \
        python3 \
        python3-dev \
        build-base
    RUN curl -sSL https://install.python-poetry.org | python3 - --preview
    ENV PATH="/root/.local/bin:$PATH"
    COPY system-test system-test
    COPY infrastructure infrastructure
    WITH DOCKER --compose infrastructure/docker-compose.yml --load=+docker-app \
        --service database \
        --service koala
        RUN sleep 5 && cd system-test && poetry install && poetry run pytest --md-report --md-report-verbose=1 system_api_test.py 
    END