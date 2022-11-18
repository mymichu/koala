from dependency_injector import containers, providers
from immudb import ImmudbClient

from koala.api.api import Api
from koala.api.user import UserApi
from koala.database.setup import DatabaseInitializer

# pylint: disable=no-member
class ContainerDatabase(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    immuclient = providers.Singleton(ImmudbClient, config.database.url)
    database = providers.Singleton(DatabaseInitializer, immuclient, config.database.name)


class ContainerApi(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    immuclient = providers.Dependency(instance_of=ImmudbClient)
    api_factory = providers.Factory(
        Api,
        client=immuclient,
    )
    api_user_factory = providers.Factory(
        UserApi,
        client=immuclient,
    )
