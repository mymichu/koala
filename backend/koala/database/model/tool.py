from dataclasses import dataclass
from typing import List

from immudb import ImmudbClient

from . import DataBaseEntity, Entity


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


def get_by(client: ImmudbClient, **kwargs) -> List[ToolID]:
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
    return [ToolID(*item) for item in resp]
