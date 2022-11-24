from dataclasses import dataclass
from datetime import datetime
from typing import List

from immudb import ImmudbClient

from .system import SystemID
from .tool import ToolID


@dataclass
class LinkSystemToolID:
    system_id: int
    system_tool_id: int
    valid: bool = False
    changed_at: datetime = datetime.now()
    identity: int = 0


class LinkSystemTool(LinkSystemToolID):
    def __init__(self, client: ImmudbClient, system_id: int, tool_system_id: int):
        super().__init__(system_id=system_id, system_tool_id=tool_system_id)
        self._client = client

    def add(self) -> None:
        response_system = self._client.sqlQuery(
            """
            SELECT COUNT(*) FROM entity WHERE id=@system_id AND is_system=TRUE;
            """,
            params={"system_id": self.system_id},
        )
        response_system_tool = self._client.sqlQuery(
            """
            SELECT COUNT(*) FROM entity WHERE id=@system_tool_id;
            """,
            params={"system_tool_id": self.system_tool_id},
        )

        if response_system[0][0] != 1 or response_system_tool[0][0] != 1:
            raise ValueError("System or Tool does not exist")

        self._client.sqlExec(
            """
            BEGIN TRANSACTION;
            INSERT INTO  entitylinker(system_id, system_tool_id, valid, changed_at)
            VALUES (@system_id, @system_tool_id, TRUE, NOW());
            COMMIT;
            """,
            params={
                "system_id": self.system_id,
                "system_tool_id": self.system_tool_id,
            },
        )

    def remove(self) -> None:
        self._client.sqlExec(
            """
            BEGIN TRANSACTION;
            INSERT INTO  entitylinker(ssystem_id, system_tool_id, valid, changed_at)
            VALUES (@system_id , @system_tool_id, FALSE, NOW());
            COMMIT;
                """,
            params={
                "system_id": self.system_id,
                "system_tool_id": self.system_tool_id,
            },
        )


class LinkSystemToolMonitor:
    def __init__(self, client: ImmudbClient):
        self._client = client

    def get_linked_tools(self, system_id: int) -> List[ToolID]:
        response = self._client.sqlQuery(
            """
            SELECT COUNT(*) FROM entity WHERE id=@system_id AND is_system=TRUE;
            """,
            params={"system_id": system_id},
        )

        if response[0][0] != 1:
            raise ValueError("System does not exist")

        tools_linked = self._client.sqlQuery(
            """
            SELECT entity.id, entity.name, entity.version_major, entity.purpose
            FROM entitylinker AS linker
            INNER JOIN entity ON entity.id = linker.system_tool_id AND entity.is_system = FALSE
            WHERE linker.system_id = @system_id AND linker.valid = TRUE;
            """,
            params={"system_id": system_id},
        )
        # TODO: return tool id in the future
        return [
            ToolID(name=tool_name, version_major=tool_version, purpose=tool_purpose, identity=identity)
            for (identity, tool_name, tool_version, tool_purpose) in tools_linked
        ]

    def get_linked_systems(self, tool_id: int) -> List[SystemID]:

        response = self._client.sqlQuery(
            """
            SELECT COUNT(*) FROM entity WHERE id=@tool_id AND is_system=FALSE;
            """,
            params={"tool_id": tool_id},
        )

        if response[0][0] != 1:
            raise ValueError("Tool does not exist")

        systems_linked = self._client.sqlQuery(
            """
            SELECT entity.id, entity.name, entity.version_major, entity.purpose
            FROM entitylinker AS linker
            INNER JOIN entity ON entity.id = linker.system_id AND entity.is_system = TRUE
            WHERE linker.system_tool_id = @tool_id AND linker.valid = TRUE;
            """,
            params={
                "tool_id": tool_id,
            },
        )
        return [
            SystemID(name=system_name, version_major=system_major_version, purpose=purpose, identity=identity)
            for (identity, system_name, system_major_version, purpose) in systems_linked
        ]
