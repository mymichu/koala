from dataclasses import dataclass
from datetime import datetime

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
    def __init__(self, client: ImmudbClient, entity: Entity) -> None:
        self._client = client
        self._entity = entity

    def insert(self) -> None:
        self._client.sqlExec(
            """
        BEGIN TRANSACTION;
            INSERT INTO entity (name, version_major, purpose, changed_at, is_system, gmp_relevant)
            VALUES (@name, @version_major,@purpose, NOW(), @is_system, @gmp_relevant);
        COMMIT;
        """,
            params={
                "name": self._entity.name,
                "version_major": self._entity.version_major,
                "purpose": self._entity.purpose,
                "is_system": self._entity.is_system,
                "gmp_relevant": self._entity.gmp_relevant,
            },
        )

    def get_id(self) -> int:
        resp = self._client.sqlQuery(
            """
                SELECT id FROM entity
                WHERE name = @name
                AND version_major = @version_major
                AND purpose = @purpose
                AND is_system = @is_system;
                """,
            params={
                "name": self._entity.name,
                "version_major": self._entity.version_major,
                "purpose": self._entity.purpose,
                "is_system": self._entity.is_system,
            },
        )
        if len(resp) != 1:
            raise Exception("Entity not found")
        return int(resp[0][0])
