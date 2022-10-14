from immudb import ImmudbClient
from uuid import uuid4

URL = "localhost:3322"  # ImmuDB running on your machine
LOGIN = "immudb"        # Default username
PASSWORD = "immudb"     # Default password
DB = b"defaultdb"       # Default database name (must be in bytes)

def main():
    client = ImmudbClient(URL)
    client.login(LOGIN, PASSWORD, database = DB)

    client.sqlExec("""
        CREATE TABLE IF NOT EXISTS systemToTools(
    system_id INT,
    tool_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (system_id, tool_id)
);""")
        
    client.sqlExec("""
        CREATE TABLE IF NOT EXISTS entity(
    id INTEGER AUTO_INCREMENT,
    name VARCHAR,
    version VARCHAR,
    purpose VARCHAR,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_system BOOLEAN,
    PRIMARY KEY id
);""")

    client.sqlExec("""
        CREATE TABLE IF NOT EXISTS change(
    id INTEGER AUTO_INCREMENT,
    change VARCHAR,
    entity_id INT,
);""")

if __name__ == "__main__":
    main()