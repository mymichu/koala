from dataclasses import dataclass
from immudb import ImmudbClient

from . import Entity, DataBaseEntity


@dataclass
class SystemID(Entity):
    is_system: bool = True


# All Systems are GMP relevant
class System(SystemID):
    def __init__(self, client: ImmudbClient, name: str, version_major: int, purpose: str) -> None:
        super().__init__(name=name, version_major=version_major, purpose=purpose)
        self._client = client
        self._entity = DataBaseEntity(client=client)

    def add(self) -> None:
        self._entity.insert(
            SystemID(
                name=self.name,
                version_major=self.version_major,
                purpose=self.purpose,
            )
        )
