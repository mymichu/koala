from dataclasses import dataclass
from datetime import datetime
from typing import Any, List

from immudb import ImmudbClient


@dataclass(unsafe_hash=True)
class Entity:
    name: str
    version_major: int
    purpose: str
    is_system: bool
    gmp_relevant: bool = True
    change_at: datetime = datetime.now()
    identity: int = 0


class DataBaseEntity:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def insert(self, entiy: Entity) -> None:
        self._client.sqlExec(
            f"""
        BEGIN TRANSACTION;
            INSERT INTO entity (name, version_major, purpose, changed_at, is_system, gmp_relevant)
            VALUES ('{entiy.name}', {entiy.version_major},'{entiy.purpose}', NOW(), {entiy.is_system}, {entiy.gmp_relevant});
        COMMIT;
        """
        )

    def is_valid(self, name: str, version_major: int) -> bool:
        resp = self._client.sqlQuery(
            f"""
        SELECT * FROM entity
        WHERE name = '{name}'
        AND version_major = {version_major};
        """
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
