from immudb import ImmudbClient
from uuid import uuid4


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
            tool_owner_name VARCHAR[128], 
            tool_owner_major_version INTEGER,
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
                PRIMARY KEY (name,version_major)
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


# uuid_gcc = str(uuid4())
# uuid_clang = str(uuid4())
# uuid_system1 = str(uuid4())

# resp = client.sqlExec(
#    f"""
#    BEGIN TRANSACTION;

#    INSERT INTO entity (name, version, uuid, purpose, changed_at, is_system)
#        VALUES ('GCC', '1.1.0', '{uuid_gcc}','Compiler for C/C++', NOW(), FALSE);
#    INSERT INTO entity (name, version, uuid, purpose, changed_at, is_system)
#       VALUES ('CLANG', '10.3.0','{uuid_clang}', 'Compiler for C/C++', NOW(), FALSE);
#   INSERT INTO entity (name, version, uuid, purpose, changed_at, is_system)
#       VALUES ('SYSTEM1', '1.2.0', '{uuid_system1}', 'Toolchain for embedded devices', NOW(), TRUE);
#   INSERT INTO systemtool (system_id, tool_id, created_at)
#       VALUES ('{uuid_system1}', '{uuid_clang}', NOW());
#   INSERT INTO systemtool (system_id, tool_id, created_at)
#       VALUES ('{uuid_system1}', '{uuid_gcc}', NOW());
#
#    COMMIT;
# """
# )
