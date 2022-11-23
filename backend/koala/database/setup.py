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
            print(f"Deleting database {self._name}")
            self._client.unloadDatabase(str.encode(self._name))
            self._client.deleteDatabase(str.encode(self._name))

    def setup_tables(self) -> None:
        self._client.sqlExec(
            """
            CREATE TABLE IF NOT EXISTS entitylinker (
            id INTEGER AUTO_INCREMENT,
            system_id INTEGER,
            system_tool_id INTEGER,
            valid BOOLEAN,
            changed_at TIMESTAMP,
            PRIMARY KEY (id)
            );"""
        )

        self._client.sqlExec(
            """
            CREATE TABLE IF NOT EXISTS entity (
                id INTEGER AUTO_INCREMENT,
                name VARCHAR[256],
                version_major INTEGER,
                purpose VARCHAR[64],
                changed_at TIMESTAMP,
                is_system BOOLEAN,
                is_active BOOLEAN,
                gmp_relevant BOOLEAN,
                PRIMARY KEY id
                );"""
        )

        self._client.sqlExec(
            """
            CREATE UNIQUE INDEX ON entity(name,version_major,purpose);
            """
        )

        self._client.sqlExec(
            """
            CREATE TABLE IF NOT EXISTS change (
                 requester_id INTEGER,
                 reviewer_id INTEGER,
                 creation_date TIMESTAMP,
                 id INTEGER AUTO_INCREMENT,
                 description VARCHAR[256],
                 entity_name VARCHAR[256],
                 entity_major_version INTEGER,
                 PRIMARY KEY id
                );"""
        )

        self._client.sqlExec(
            """
            CREATE TABLE IF NOT EXISTS document (
                id INTEGER AUTO_INCREMENT,
                name VARCHAR[256],
                path VARCHAR[256],
                creation_date TIMESTAMP,
                is_released BOOLEAN,
                PRIMARY KEY id
                );"""
        )

        self._client.sqlExec(
            """
            CREATE TABLE IF NOT EXISTS entity_x_document (
                id INTEGER AUTO_INCREMENT,
                document_id INTEGER,
                entity_id INTEGER,
                creation_date TIMESTAMP,
                PRIMARY KEY id
                );"""
        )

        self._client.sqlExec(
            """
            CREATE TABLE IF NOT EXISTS user (
                name VARCHAR[256],
                first_name VARCHAR[256],
                email VARCHAR[256],
                active BOOLEAN,
                created_at TIMESTAMP,
                PRIMARY KEY email
                );"""
        )

        self._client.sqlExec(
            """
            CREATE TABLE IF NOT EXISTS entity_ownership (
                id INTEGER AUTO_INCREMENT,
                entity_id INTEGER,
                owner_email VARCHAR[256],
                active BOOLEAN,
                PRIMARY KEY id
                );"""
        )
