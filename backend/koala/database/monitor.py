from json import tool
from typing import List

from immudb import ImmudbClient
from typing import Any

from .entity import Entity, SystemID, ToolID


def _in(entitylinker: tuple, entity: tuple) -> bool:
    name = entity[0]

    for link_name in entitylinker:
        if name == link_name[0]:
            return True

    return False


class Monitor:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def get_all_systems(self) -> List[SystemID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity WHERE is_system = TRUE;
        """
        )
        return list(map(lambda x: SystemID(*x), resp))

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
            f"""
        SELECT name, version_major, purpose, gmp_relevant FROM entity
        WHERE name = '{name}' AND is_system = FALSE;
        """
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

    def get_documents(self, entity: Any) -> List[Entity]:
        entities = self._client.sqlQuery(
            """
            SELECT name, version_major, purpose, is_system FROM entity;
            """
        )

        tool_links = self._client.sqlQuery(
            f"""
        SELECT tool_name, system_name FROM entitylinker
        WHERE system_name = '{entity.name}';
        """
        )

        system_links = self._client.sqlQuery(
            f"""
        SELECT system_name, tool_name FROM entitylinker
        WHERE tool_name = '{entity.name}';
        """
        )

        links = tool_links + system_links

        entities = [entity for entity in entities if _in(links, entity)]

        result = []
        for name, version_major, purpose, is_system in entities:
            if is_system:
                result.append(SystemID(name, version_major, purpose))
            else:
                result.append(ToolID(name, version_major, purpose))

        return result
