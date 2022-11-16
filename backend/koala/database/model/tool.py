from dataclasses import dataclass
from typing import Any, List

from immudb import ImmudbClient

from .entity import DataBaseEntity, Entity
from .entity import get_by as get_entity_by


@dataclass
class ToolID(Entity):
    is_system: bool = False


# pylint: disable=too-many-arguments
class Tool(ToolID):
    def __init__(
        self, client: ImmudbClient, name: str, version_major: int, purpose: str, gmp_relevant: bool = True
    ) -> None:
        super().__init__(name=name, version_major=version_major, purpose=purpose, gmp_relevant=gmp_relevant)
        self._client = client
        self._entity = DataBaseEntity(client=client)

    def add(self) -> None:
        self._entity.insert(
            ToolID(
                name=self.name,
                version_major=self.version_major,
                purpose=self.purpose,
                gmp_relevant=self.gmp_relevant,
            )
        )


def get_by(client: ImmudbClient, **kwargs: Any) -> List[ToolID]:
    entities = get_entity_by(client, **kwargs)
    return [ToolID(*item) for item in entities]
