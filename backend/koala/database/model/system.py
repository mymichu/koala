from dataclasses import dataclass, field
from typing import Any, List

from immudb import ImmudbClient

from .entity import DataBaseEntity, Entity


@dataclass
class SystemID(Entity):
    is_system: bool = field(default=True, init=False)


# All Systems are GMP relevant
# pylint: disable=too-many-arguments
class System(SystemID):
    def __init__(
        self, client: ImmudbClient, name: str = "", version_major: int = -1, purpose: str = "", identity: int = -1
    ) -> None:
        super().__init__(name=name, version_major=version_major, purpose=purpose, gmp_relevant=True)
        self._client = client
        self._entity = DataBaseEntity(
            client=client,
            entity=SystemID(
                name=self.name,
                version_major=self.version_major,
                purpose=self.purpose,
                gmp_relevant=self.gmp_relevant,
                identity=identity,
            ),
        )

    def add(self) -> None:
        self._entity.insert()

    def get_id(self) -> int:
        return self._entity.get_id()

    def is_active(self) -> bool:
        return self._entity.is_active()

    def set_active(self, active: bool) -> None:
        return self._entity.set_active_status(active)


class SystemMonitor:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    # The order of the columns matters: id, name, version_major, purpose, changed_at, gmp_relevant
    def _convert_query_system_id(self, resp: Any) -> List[SystemID]:
        systems: List[SystemID] = []
        for item in resp:
            (identiy, name, version_major, purpose, changed_at, gmp_relevant) = item
            system = SystemID(
                name=name,
                version_major=version_major,
                purpose=purpose,
                change_at=changed_at,
                gmp_relevant=gmp_relevant,
                identity=identiy,
            )
            systems.append(system)
        return systems

    def get_all_systems(self) -> List[SystemID]:
        resp = self._client.sqlQuery(
            """
        SELECT id, name, version_major, purpose, changed_at, gmp_relevant FROM entity WHERE is_system = TRUE;
        """
        )

        return self._convert_query_system_id(resp)
