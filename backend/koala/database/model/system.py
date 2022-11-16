from dataclasses import dataclass
from typing import List

from immudb import ImmudbClient

from . import DataBaseEntity, Entity


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


def get_by(client: ImmudbClient, **kwargs) -> List[SystemID]:
    query = "SELECT name, version_major, purpose, is_system, gmp_relevant, changed_at, id FROM entity"
    sep = " WHERE "

    for key, value in kwargs.items():
        if isinstance(value, str):
            condition = f"{sep}{key}='{value}'"
        else:
            condition = f"{sep}{key}={value}"

        sep = " AND "
        query += condition

    resp = client.sqlQuery(query)
    return [SystemID(*item) for item in resp]
