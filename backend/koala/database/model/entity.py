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


# pylint: disable=too-many-arguments
class DataBaseEntity(Entity):
    def __init__(
        self,
        client: ImmudbClient,
        name: str,
        version_major: int,
        purpose: str,
        is_system: bool,
        gmp_relevant: bool,
        change_at: datetime = datetime.now(),  # TODO: Not sure if this is needed
        identity: int = -1,
    ) -> None:
        super().__init__(
            name=name,
            version_major=version_major,
            purpose=purpose,
            is_system=is_system,
            gmp_relevant=gmp_relevant,
            change_at=change_at,
            identity=identity,
        )
        self._client = client

    def add(self) -> None:
        self._check_name_version_purpose()
        self._client.sqlExec(
            """
        BEGIN TRANSACTION;
            INSERT INTO entity (name, version_major, purpose, changed_at, is_system, gmp_relevant)
            VALUES (@name, @version_major,@purpose, NOW(), @is_system, @gmp_relevant);
        COMMIT;
        """,
            params={
                "name": self.name,
                "version_major": self.version_major,
                "purpose": self.purpose,
                "is_system": self.is_system,
                "gmp_relevant": self.gmp_relevant,
            },
        )

    def _check_name_version_purpose(self) -> None:
        if len(self.name) == 0:
            raise ValueError("Entity name cannot be empty")
        if len(self.purpose) == 0:
            raise ValueError("Entity purpose cannot be empty")
        if self.version_major < 0:
            raise ValueError("Entity version cannot be negative")

    def _check_id(self) -> None:
        if self.identity == -1:
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
                "name": self.name,
                "version_major": self.version_major,
                "purpose": self.purpose,
                "is_system": self.is_system,
            },
        )
        if len(resp) != 1:
            raise Exception("Entity not found")
        self.identity = int(resp[0][0])
        return self.identity

    def is_active(self) -> bool:
        self._check_id()

        resp = self._client.sqlQuery(
            """
                SELECT is_active FROM entity
                WHERE id = @identity;
                """,
            params={
                "identity": self.identity,
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
            params={"id": self.identity, "is_active": is_active},
        )
