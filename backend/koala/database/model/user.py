from dataclasses import dataclass

from immudb import ImmudbClient


@dataclass
class UserData:
    name: str
    first_name: str
    email: str
    active: bool = True
    identity: int = -1


class User:
    def __init__(self, client: ImmudbClient, user: UserData) -> None:
        self._client = client
        self._user = user

    def add(self) -> None:
        self._client.sqlExec(
            """
        BEGIN TRANSACTION;
            INSERT INTO user(name, first_name, active, email, created_at)
            VALUES (@name, @first_name, @active, @email ,NOW());
        COMMIT;
        """,
            params={
                "name": self._user.name,
                "first_name": self._user.first_name,
                "active": self._user.active,
                "email": self._user.email,
            },
        )

    def disable(self) -> None:
        self._client.sqlExec(
            """
        BEGIN TRANSACTION;
            UPSERT INTO user(email, active)
            VALUES (@email, FALSE);
        COMMIT;
        """,
            params={
                "email": self._user.email,
            },
        )

    def get_id(self) -> int:
        resp = self._client.sqlQuery(
            """
            SELECT id FROM user
            WHERE email=@email
            """,
            params={"email": self._user.email},
        )
        if len(resp) != 1:
            raise Exception("Document not found")
        self._user.identity = int(resp[0][0])
        return self._user.identity
