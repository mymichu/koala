from typing import List

from immudb import ImmudbClient
from typing import Any

from .entity import SystemID, ToolID


def _to_tools(response: Any) -> List[ToolID]:
    return [SystemID(name, version_major, purpose) for (name, version_major, purpose) in resp]


class Monitor:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def get_all_systems(self) -> List[SystemID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity WHERE is_system = TRUE;
        """
        )
        return _to_tools(resp)

    def unlinked_tools(self) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity
        WHERE is_system = FALSE
        AND name NOT IN (SELECT tool_name FROM entitylinker);
        """
        )
        return []

    def get_all_tools(self) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity WHERE is_system = FALSE;
        """
        )
        return _to_tools(resp)

    def get_tools(self, name: str) -> List[ToolID]:
        resp = self._client.sqlQuery(
            f"""
        SELECT name, version_major, purpose FROM entity
        WHERE name = '{name}' AND is_system = FALSE;
        """
        )
        return _to_tools(resp)
