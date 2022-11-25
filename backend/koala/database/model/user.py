from dataclasses import dataclass
from typing import Any

from immudb import ImmudbClient


@dataclass
class UserData:
    name: str = ""
    first_name: str = ""
    email: str = ""
    active: bool = True
    identity: int = -1


class User:
    def __init__(self, client: ImmudbClient, user: UserData) -> None:
        self._client = client
        self._user = user

    def _check_id(self) -> None:
        if self._user.identity == -1:
            raise Exception("User not found")

    def _check_data(self) -> None:
        if len(self._user.name) == 0 or len(self._user.first_name) == 0 or len(self._user.email) == 0:
            raise ValueError("User name,first_name, email cannot be empty")

    # The order of the columns matters: identity, name, first_name, active, email, created_at
    def _convert_query_user_data(self, resp: Any) -> UserData:
        (identity, name, first_name, active, email, _) = resp[0]
        user = UserData(
            name=name,
            first_name=first_name,
            email=email,
            active=active,
            identity=identity,
        )
        return user

    def add(self) -> None:
        self._check_data()
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
        self._check_id()
        self._client.sqlExec(
            """
        BEGIN TRANSACTION;
            UPSERT INTO user(id, active)
            VALUES (@id, FALSE);
        COMMIT;
        """,
            params={
                "id": self._user.identity,
            },
        )

    def get_id(self) -> int:
        self._check_data()
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

    def get(self) -> UserData:
        self._check_id()
        resp = self._client.sqlQuery(
            """
            SELECT id, name, first_name, active, email, created_at FROM user
            WHERE id=@id
            """,
            params={"id": self._user.identity},
        )
        return self._convert_query_user_data(resp)
