from dependency_injector import containers, providers
from example.database.tool import DataBaseTools, DataBaseToolsInterface, DatabaseToolsMocks


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    if config.dummy:
        dbTools = providers.Singleton(DatabaseToolsMocks)
    else:
        dbTools = providers.Singleton(DataBaseTools)
