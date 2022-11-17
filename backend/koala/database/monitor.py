from typing import List

from immudb import ImmudbClient

from .model.system import SystemID
from .model.tool import ToolID


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
