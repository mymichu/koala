import os

import pytest
from dependency_injector import providers

from koala.factory import ContainerApi, ContainerDatabase

host = os.getenv("IMMUDB_HOST", "database")
print(f"DATABASE: {host}")
URL = f"{host}:3322"
USERNAME = "immudb"
PASSWORD = "immudb"


@pytest.fixture(scope="function")
def koala_api(request):
    config = providers.Configuration()
    database_name = request.node.name.replace("_", "")
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
    yield api_container
    database.delete()
    client = database_container.immuclient()
    client.logout()
    client.shutdown()
