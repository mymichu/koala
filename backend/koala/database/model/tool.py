from dataclasses import dataclass

from immudb import ImmudbClient
from . import Entity, DataBaseEntity


@dataclass
class ToolID(Entity):
    is_system: bool = False


class Tool:
    def __init__(
        self, client: ImmudbClient, name: str, version_major: int, purpose: str, gmp_relevant: bool = True
    ) -> None:
        self._client = client
        self._entity = DataBaseEntity(client=client)
        self.name = name
        self.version_major = version_major
        self.purpose = purpose
        self.gmp_relevant = gmp_relevant

    def add(self) -> None:
        self._entity.insert(
            ToolID(
                name=self.name,
                version_major=self.version_major,
                purpose=self.purpose,
                gmp_relevant=self.gmp_relevant,
            )
        )
