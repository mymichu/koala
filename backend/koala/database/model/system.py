from dataclasses import dataclass
from typing import Any, List

from immudb import ImmudbClient

from .entity import DataBaseEntity, Entity
from .entity import get_by as get_entity_by


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


def get_by(client: ImmudbClient, **kwargs: Any) -> List[SystemID]:
    entities = get_entity_by(client, **kwargs)
    return [SystemID(*item) for item in entities]
