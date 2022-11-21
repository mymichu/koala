import os

import uvicorn
from dependency_injector import providers
from fastapi import FastAPI

from koala.endpoints import system, tools
from koala.factory import ContainerApi, ContainerDatabase

host = os.getenv("IMMUDB_HOST", "database")
print(f"DATABASE: {host}")
URL = f"{host}:3322"
USERNAME = os.getenv("IMMUDB_USR", "immudb")
PASSWORD = os.getenv("IMMUDB_PW", "immudb")


def create_application() -> FastAPI:
    config = providers.Configuration()
    database_name = "test"
    config.from_dict(
        {
            "database": {"url": URL, "name": database_name, "username": USERNAME, "password": PASSWORD},
        },
    )
    database_container = ContainerDatabase(config=config)
    api_container = ContainerApi(config=config, immuclient=database_container.immuclient)
    immuclient = database_container.immuclient()
    immuclient.login(username=USERNAME, password=PASSWORD)
    database = database_container.database()
    database.delete()
    database.create_and_use()
    database.setup_tables()
    app = FastAPI()
    # This is after example of dependecy injection framework -> mypy seems to have a problem with this
    app.container = api_container  # type: ignore
    app.include_router(tools.router)
    app.include_router(system.router)
    return app


def main() -> None:
    app = create_application()
    uvicorn.run(app, port=8002)


if __name__ == "__main__":
    main()
