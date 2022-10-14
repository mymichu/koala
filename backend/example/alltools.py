from immudb import ImmudbClient
from uuid import uuid4

URL = "database:3322"  # ImmuDB running on your machine
LOGIN = "immudb"  # Default username
PASSWORD = "immudb"  # Default password
DB = b"defaultdb"  # Default database name (must be in bytes)


def all_tools_for_given_sde(client):
    sde = "SYSTEM1"

    result = client.sqlQuery(
        f"""
        SELECT uuid FROM entity WHERE name = '{sde}'; 
        """
    )

    (uuid,) = result[0]
    result = client.sqlQuery(
        f"""
        SELECT TOOL_ID FROM systemtool WHERE SYSTEM_ID = '{uuid}'; 
        """
    )
    print("Tools for system", sde, "are:")

    for item in result:
        result = client.sqlQuery(
            f"""
            SELECT NAME FROM entity WHERE UUID = '{item[0]}'; 
            """
        )
        print(result[0][0])
        
        

if __name__ == "__main__":
    client = ImmudbClient(URL)
    client.login(LOGIN, PASSWORD, database=DB)

    all_tools_for_given_sde(client)
