import os

import uvicorn
from dependency_injector import providers
from fastapi import FastAPI

from koala.database.setup import DatabaseInitializer
from koala.endpoints import change, document, system, tools, user
from koala.factory import ContainerApi, ContainerDatabase

host = os.getenv("IMMUDB_HOST", "database")
print(f"DATABASE: {host}")
URL = f"{host}:3322"
USERNAME = os.getenv("IMMUDB_USR", "immudb")
PASSWORD = os.getenv("IMMUDB_PW", "immudb")
HOST = os.getenv("HOST", "127.0.0.1")
DATABASE_SETUP_MODE = os.getenv("RESTART_DB", "RESET")  # RESET, KEEP


def setup_database(database: DatabaseInitializer) -> None:
    if DATABASE_SETUP_MODE == "RESET":
        database.delete()
    database.create_and_use()
    if DATABASE_SETUP_MODE == "RESET":
        database.setup_tables()


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
    setup_database(database)
    app = FastAPI()
    # This is after example of dependecy injection framework -> mypy seems to have a problem with this
    app.container = api_container  # type: ignore
    app.include_router(tools.router)
    app.include_router(system.router)
    app.include_router(document.router)
    app.include_router(user.router)
    app.include_router(change.router)
    return app


def main() -> None:
    app = create_application()
    uvicorn.run(app, host=HOST, port=8002)


if __name__ == "__main__":
    main()
