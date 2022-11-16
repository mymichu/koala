from dataclasses import dataclass
from datetime import datetime
from typing import List

from immudb import ImmudbClient

from . import SystemID, ToolID


@dataclass
class LinkSystemToolID:
    system_name: str
    system_major_version: int
    tool_name: str
    tool_major_version: int
    valid: bool = False
    changed_at: datetime = datetime.now()
    id: int = 0


class LinkSystemTool(LinkSystemToolID):
    def __init__(self, client: ImmudbClient, system: SystemID, tool: ToolID):
        super().__init__(
            system_name=system.name,
            system_major_version=system.version_major,
            tool_name=tool.name,
            tool_major_version=tool.version_major,
        )
        self._client = client

    def add(self) -> None:
        self._client.sqlExec(
            f"""
            BEGIN TRANSACTION;
            INSERT INTO  entitylinker(system_name, system_major_version, tool_name, tool_major_version, valid, changed_at)
            VALUES ('{self.system_name}', {self.system_major_version}, '{self.tool_name}',{self.tool_major_version}, TRUE, NOW());
            COMMIT;
            """
        )

    def remove(self) -> None:
        self._client.sqlExec(
            f"""
            BEGIN TRANSACTION;
            INSERT INTO  entitylinker(system_name, tool_ownerversion_major, tool_name, toolversion_major, valid, changed_at)
            VALUES ('{self.system_name}', {self.system_major_version}, '{self.tool_name}',{self.tool_major_version}, FALSE, NOW());
            COMMIT;
                """
        )


def get_linked_tools(client: ImmudbClient, system: SystemID) -> List[ToolID]:
    tools_linked = client.sqlQuery(
        f"""
        SELECT linker.tool_name, linker.tool_major_version, tool.purpose
        FROM entitylinker AS linker
        INNER JOIN entity AS tool ON linker.tool_name = tool.name AND linker.tool_major_version = tool.version_major
        WHERE linker.system_name = '{system.name}' AND linker.system_major_version = {system.version_major} AND linker.valid = TRUE AND tool.is_system=FALSE;
        """
    )

    return [
        ToolID(name=tool_name, version_major=tool_version, purpose=tool_purpose)
        for (tool_name, tool_version, tool_purpose) in tools_linked
    ]


def get_linked_systems(client: ImmudbClient, tool: ToolID) -> List[SystemID]:
    systems_linked = client.sqlQuery(
        f"""
        SELECT linker.system_name, linker.system_major_version, system.purpose
        FROM entitylinker AS linker
        INNER JOIN entity AS system ON linker.system_name = system.name AND linker.system_major_version = system.version_major
        WHERE linker.tool_name = '{tool.name}' AND linker.tool_major_version = {tool.version_major} AND valid = TRUE AND system.is_system=TRUE;
        """
    )
    return [
        SystemID(name=system_name, version_major=system_major_version, purpose=purpose)
        for (system_name, system_major_version, purpose) in systems_linked
    ]
