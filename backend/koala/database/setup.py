from uuid import uuid4

from immudb import ImmudbClient


class DatabaseInitializer:
    def __init__(self, client: ImmudbClient, name: str) -> None:
        self._client = client
        self._name = name

    def create_and_use(self) -> None:
        if self._name not in self._client.databaseList():
            self._client.createDatabase(str.encode(self._name))
        self._client.useDatabase(str.encode(self._name))

    def delete(self) -> None:
        if self._name in self._client.databaseList():
            self._client.unloadDatabase(str.encode(self._name))
            self._client.deleteDatabase(str.encode(self._name))

    def setup_tables(self) -> None:
        self._client.sqlExec(
            """
            CREATE TABLE IF NOT EXISTS entitylinker (
            id INTEGER AUTO_INCREMENT,
            system_name VARCHAR[128],
            system_major_version INTEGER,
            tool_name VARCHAR[128],
            tool_major_version INTEGER,
            valid BOOLEAN,
            changed_at TIMESTAMP,
            PRIMARY KEY (id)
            );"""
        )

        self._client.sqlExec(
            """
            CREATE TABLE IF NOT EXISTS entity (
                name VARCHAR[256],
                version_major INTEGER,
                purpose VARCHAR[64],
                changed_at TIMESTAMP,
                is_system BOOLEAN,
                PRIMARY KEY (name,version_major,purpose)
                );"""
        )

        self._client.sqlExec(
            """
            CREATE TABLE IF NOT EXISTS change (
                id INTEGER AUTO_INCREMENT,
                change VARCHAR[256],
                entity_name VARCHAR[256],
                entity_major_version INTEGER,
                PRIMARY KEY id
                );"""
        )
