from immudb import ImmudbClient
from uuid import uuid4

URL = "database:3322"  # ImmuDB running on your machine
LOGIN = "immudb"  # Default username
PASSWORD = "immudb"  # Default password
DB = b"defaultdb"  # Default database name (must be in bytes)


def main():
    client = ImmudbClient(URL)
    client.login(LOGIN, PASSWORD, database=DB)

    client.sqlExec(
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

    client.sqlExec(
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

    client.sqlExec(
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


if __name__ == "__main__":
    main()

#
#
#
#
#
#
#
#
