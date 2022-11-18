from dataclasses import dataclass
from datetime import datetime
from typing import Any, List

from immudb import ImmudbClient


@dataclass
class EntityKey:
    name: str
    version_major: int
    purpose: str


@dataclass
class Entity(EntityKey):
    is_system: bool = False
    gmp_relevant: bool = True
    change_at: datetime = datetime.now()
    identity: int = -1


class DataBaseEntity:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def insert(self, entiy: Entity) -> None:
        self._client.sqlExec(
            """
        BEGIN TRANSACTION;
            INSERT INTO entity (name, version_major, purpose, changed_at, is_system, gmp_relevant)
            VALUES (@name, @version_major,@purpose, NOW(), @is_system, @gmp_relevant);
        COMMIT;
        """,
            params={
                "name": entiy.name,
                "version_major": entiy.version_major,
                "purpose": entiy.purpose,
                "is_system": entiy.is_system,
                "gmp_relevant": entiy.gmp_relevant,
            },
        )

    def is_valid(self, name: str, version_major: int) -> bool:
        resp = self._client.sqlQuery(
            """
        SELECT * FROM entity
        WHERE name = @name
        AND version_major = @version_major;
        """,
            params={
                "name": name,
                "version_major": version_major,
            },
        )
        return len(resp) == 1


def get_by(client: ImmudbClient, **kwargs: Any) -> List:
    query = "SELECT name, version_major, purpose, is_system, gmp_relevant, changed_at, id FROM entity"
    sep = " WHERE "
    for key, value in kwargs.items():
        if isinstance(value, str):
            condition = f"{sep}{key}='{value}'"
        else:
            condition = f"{sep}{key}={value}"
        sep = " AND "
        query += condition
    return list(client.sqlQuery(query))
