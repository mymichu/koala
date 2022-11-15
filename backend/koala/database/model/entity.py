from dataclasses import dataclass

from immudb import ImmudbClient


@dataclass(unsafe_hash=True)
class Entity:
    name: str
    version_major: int
    purpose: str
    is_system: bool
    gmp_relevant: bool = True


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
