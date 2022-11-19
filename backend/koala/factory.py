from dependency_injector import containers, providers
from immudb import ImmudbClient

from koala.api.document import DocumentApi
from koala.api.system import SystemApi
from koala.api.tool import ToolApi
from koala.api.user import UserApi
from koala.database.setup import DatabaseInitializer


# pylint: disable=no-member
class ContainerDatabase(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    immuclient: providers.Singleton = providers.Singleton(ImmudbClient, config.database.url)
    database: providers.Singleton = providers.Singleton(DatabaseInitializer, immuclient, config.database.name)


class ContainerApi(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".endpoints.tools", ".endpoints.system"])

    config = providers.Configuration(strict=True)
    immuclient = providers.Dependency(instance_of=ImmudbClient)

    api_document_factory = providers.Factory(
        DocumentApi,
        client=immuclient,
    )
    api_system_factory = providers.Factory(
        SystemApi,
        client=immuclient,
    )
    api_tool_factory = providers.Factory(
        ToolApi,
        client=immuclient,
    )
    api_user_factory = providers.Factory(
        UserApi,
        client=immuclient,
    )
