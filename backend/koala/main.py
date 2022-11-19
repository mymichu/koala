import os

import uvicorn
from dependency_injector import providers
from fastapi import FastAPI

from koala.endpoints import tools, system
from koala.factory import ContainerApi, ContainerDatabase

host = os.getenv("IMMUDB_HOST", "database")
print(f"DATABASE: {host}")
URL = f"{host}:3322"
USERNAME = "immudb"
PASSWORD = "immudb"


def create_application() -> None:
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
    app.container = api_container
    app.include_router(tools.router)
    app.include_router(system.router)
    return app


def main():
    app = create_application()
    uvicorn.run(app, port=8002)


if __name__ == "__main__":
    main()
