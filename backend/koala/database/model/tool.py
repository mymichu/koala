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


def _in(entitylinker: tuple, entity: tuple) -> bool:
    name = entity[0]

    for link_name in entitylinker:
        if name == link_name[0]:
            return True

    return False


class ToolMonitor:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def unlinked_tools(self) -> List[ToolID]:
        # TODO: This should be done by database with
        # SELECT name, version_major, purpose FROM entity
        # WHERE is_system = FALSE
        # AND name NOT IN (SELECT tool_name FROM entitylinker);
        tools = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity WHERE is_system = FALSE;
        """
        )

        links = self._client.sqlQuery(
            """
        SELECT tool_name FROM entitylinker;
        """
        )

        resp = [tool for tool in tools if not _in(links, tool)]

        return list(map(lambda x: ToolID(*x), resp))

    def get_all_tools(self) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity WHERE is_system = FALSE;
        """
        )
        return list(map(lambda x: ToolID(*x), resp))

    def get_tools(self, name: str) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose, gmp_relevant FROM entity
        WHERE name = @name AND is_system = FALSE;
        """,
            params={"name": name},
        )
        return list(map(lambda x: ToolID(*x), resp))

    def get_gmp_relevant_tools(self) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity
        WHERE gmp_relevant = TRUE AND is_system = FALSE;
        """
        )
        return list(map(lambda x: ToolID(*x), resp))

    def get_non_gmp_relevant_tools(self) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity
        WHERE gmp_relevant = FALSE AND is_system = FALSE;
        """
        )
        return list(map(lambda x: ToolID(*x), resp))

    def get_all_tools_owned_by(self, email: str) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
            SELECT entity.id, entity.name, entity.version_major, entity.purpose, entity.changed_at, entity.is_system, entity.gmp_relevant
            FROM entity_ownership
            INNER JOIN entity ON entity_ownership.entity_id = entity.id
            WHERE  entity_ownership.owner_email = @user_email;
            """,
            params={"user_email": email},
        )
        tools: List[ToolID] = []
        for item in resp:
            (entity_id, name, version_major, purpose, changed_at, is_system, gmp_relevant) = item
            tool = ToolID(
                name=name,
                version_major=version_major,
                purpose=purpose,
                is_system=is_system,
                gmp_relevant=gmp_relevant,
                change_at=changed_at,
                identity=entity_id,
            )
            tools.append(tool)

        return tools
