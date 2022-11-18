from dataclasses import dataclass, field
from typing import Any, List

from immudb import ImmudbClient

from .entity import DataBaseEntity, Entity


@dataclass
class SystemID(Entity):
    is_system: bool = field(default=True, init=False)


# All Systems are GMP relevant
class System(SystemID):
    def __init__(self, client: ImmudbClient, name: str, version_major: int, purpose: str) -> None:
        super().__init__(name=name, version_major=version_major, purpose=purpose, gmp_relevant=True)
        self._client = client
        self._entity = DataBaseEntity(client=client)

    def add(self) -> None:
        self._entity.insert(
            SystemID(
                name=self.name,
                version_major=self.version_major,
                purpose=self.purpose,
                gmp_relevant=self.gmp_relevant,
            )
        )

    def get_id(self) -> int:
        resp = self._client.sqlQuery(
            """
                SELECT id FROM entity
                WHERE name = @name
                AND version_major = @version_major
                AND purpose = @purpose
                AND is_system = TRUE;
                """,
            params={
                "name": self.name,
                "version_major": self.version_major,
                "purpose": self.purpose,
            },
        )
        if len(resp) != 1:
            raise Exception("System not found")
        return int(resp[0][0])


class SystemMonitor:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def get_all_systems(self) -> List[SystemID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity WHERE is_system = TRUE;
        """
        )
        return list(map(lambda x: SystemID(*x), resp))
