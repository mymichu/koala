from immudb import ImmudbClient
from uuid import uuid4


def all_tools_for_given_sde(client, sde):
    result = client.sqlQuery(
        f"""
        SELECT uuid, version, changed_at FROM entity SINCE '2022-10-14 14:00' UNTIL NOW() WHERE name = '{sde}' ; 
        """
    )

    for item in result:
        print(item)
        uuid, sde_version, changed_at = item

        result = client.sqlQuery(
            f"""
            SELECT TOOL_ID FROM systemtool WHERE SYSTEM_ID = '{uuid}'; 
            """
        )
        print(f"Tools for system {sde} {sde_version} are ({changed_at}):")

        for item in result:
            result = client.sqlQuery(
                f"""
                SELECT NAME, VERSION FROM entity WHERE UUID = '{item[0]}'; 
                """
            )
            name, version = result[0]
            print(f"name: {name}, version: {version}")


def main():
    URL = "database:3322"  # ImmuDB running on your machine
    LOGIN = "immudb"  # Default username
    PASSWORD = "immudb"  # Default password
    DB = b"defaultdb"  # Default database name (must be in bytes)
    client = ImmudbClient(URL)
    client.login(LOGIN, PASSWORD, database=DB)

    all_tools_for_given_sde(client, "SYSTEM1")


if __name__ == "__main__":
    main()
