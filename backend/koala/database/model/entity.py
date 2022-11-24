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
        self._check_name_version_purpose()
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

    def _check_name_version_purpose(self) -> None:
        if len(self._entity.name) == 0:
            raise ValueError("Entity name cannot be empty")
        if len(self._entity.purpose) == 0:
            raise ValueError("Entity purpose cannot be empty")
        if self._entity.version_major < 0:
            raise ValueError("Entity version cannot be negative")

    def _check_id(self) -> None:
        if self._entity.identity == -1:
            raise ValueError("Entity ID not set")

    def get_id(self) -> int:
        self._check_name_version_purpose()

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
        self._entity.identity = int(resp[0][0])
        return self._entity.identity

    def is_active(self) -> bool:
        self._check_id()

        resp = self._client.sqlQuery(
            """
                SELECT is_active FROM entity
                WHERE id = @identity;
                """,
            params={
                "identity": self._entity.identity,
            },
        )
        if len(resp) != 1:
            raise Exception("Entity not found")
        return bool(resp[0][0])

    def set_active_status(self, is_active: bool) -> None:
        self._check_id()
        self._client.sqlExec(
            """
            BEGIN TRANSACTION;
                UPSERT INTO entity (id, is_active, changed_at)
                VALUES (@id, @is_active, NOW());
            COMMIT;
            """,
            params={"id": self._entity.identity, "is_active": is_active},
        )
