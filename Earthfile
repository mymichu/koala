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
    SAVE ARTIFACT koala/dist/*.whl AS LOCAL koala/dist/koala.whl

test:
    FROM +install
    ENV IMMUDB_HOST="localhost"
    COPY .devcontainer .devcontainer
    WITH DOCKER --compose .devcontainer/docker-compose.yml \
        --service database
        RUN poetry run pytest --md-report --md-report-verbose=1
    END

docker-deploy:
    FROM earthly/dind:alpine-main
    RUN apk update && apk add --no-cache \
        curl \
        python3 \
        python3-dev \
        py-pip \
        build-base
    COPY +build/koala/dist/koala.whl koala.whl
    RUN pip install koala.whl
    CMD rm -rf koala.whl
    SAVE IMAGE backend:latest