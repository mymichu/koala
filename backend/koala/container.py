from dependency_injector import containers, providers
from immudb import ImmudbClient


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    client = providers.Singleton(ImmudbClient, "database:3322")
