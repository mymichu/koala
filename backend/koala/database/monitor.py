from immudb import ImmudbClient
from typing import List

from .entity import SystemID, ToolID


class Monitor:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def get_all_systems(self) -> List[SystemID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity WHERE is_system = TRUE;
        """
        )
        return [SystemID(name, version_major, purpose) for (name, version_major, purpose) in resp]

    def get_all_tools(self) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity WHERE is_system = FALSE;
        """
        )
        return [ToolID(name, version_major, purpose) for (name, version_major, purpose) in resp]
