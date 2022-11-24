# Koala

## How to run Koala

Prerequisite: wget and Docker-Compose needs to be installed

1. Download the Docker-Compose file and start the docker-compose:
    ```bash 
    wget https://raw.githubusercontent.com/mymichu/koala/main/infrastructure/docker-compose.yml \
    && docker-compose up 
    ```

2. Now koala should be reachable. Open the Browser and connect to the [Koala-Swagger-API ](http://localhost:8002/docs)


NOTE: There could be issues when running the command above. Sometimes the port is already used by another docker instance. To stop and clean all docker instances and images, run the following command:
```bash
docker kill $(docker ps -q) && docker system prune -af
```


## Use Cases

1. Give me all the tools of a system at a given time.
2. Show me all the Systems which rely on tool Y with version X.
3. Show me all the tools which are under regulation purposes and not.
4. Show me all the changes of tool Y from a given time to a given time.
5. Show me all the changes of system A from a given time to a given time.
6. Show me all the changes end of life tools that are used by an SDE.
7. Show all related documents to tool and system.
8. Optional: Generate Reports out of information.
9. All information system data classifications are within the database.

## Development tools
immuclient login immudb - pw immudb

## SQL

./immuclient query "SELECT peoplenow.id, peoplenow.name, peoplethen.purpose, peoplenow.purpose FROM tool BEFORE now() AS peoplethen INNER JOIN tool AS peoplenow ON peoplenow.id=peoplethen.id;"


 ## Instal Docker-Compose without docker desktop on Ubuntu 20.04

Instal docker compose to a running docker engine. Therefore execute the following commands:

```bash
curl -SL https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-linux-x86_64 -o docker-compose
chmod +x docker-compose
./docker-compose version
```

## Work with koala

### Use Poetry

Use following commands inside container to check conformity before committing

Run isort

    poetry run isort . --check

Run pylint

    poetry run pylint koala --reports=y

Run black

    poetry run black . --check

Rrun flake8

    poetry run flake8 koala

Run mypy

    poetry run mypy .

Run bandit

    poetry run bandit -r koala

Run integration tests

    poetry run pytest

Create wheel package

    poetry build

### Use earthly

Run following commands to replicate pipeline locally using [Earthly](https://earthly.dev/get-earthly)

Check [ci.yml](/.github/workflows/ci.yml) file for reference of implemented Earthly commands.
