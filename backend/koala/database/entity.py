from dataclasses import dataclass
from typing import List

from immudb import ImmudbClient


@dataclass(unsafe_hash=True)
class Entity:
    name: str
    version_major: int
    purpose: str
    is_system: bool


@dataclass
class SystemID(Entity):
    is_system: bool = True


@dataclass
class ToolID(Entity):
    is_system: bool = False


class DataBaseEntity:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def insert(self, entiy: Entity) -> None:
        self._client.sqlExec(
            f"""
        BEGIN TRANSACTION;
            INSERT INTO entity (name, version_major, purpose, changed_at, is_system)
            VALUES ('{entiy.name}', {entiy.version_major},'{entiy.purpose}', NOW(), {entiy.is_system });
        COMMIT;
        """
        )

    def is_valid(self, name: str, version_major: int) -> bool:
        resp = self._client.sqlQuery(
            f"""
        SELECT * FROM entity WHERE name = '{name}' AND version_major = {version_major};
        """
        )
        return len(resp) == 1


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

    def getname(self) -> str:
        return self.name

    def get_version(self) -> int:
        return self.version_major

    def getpurpose(self) -> str:
        return self.purpose

    def _in_database(self) -> bool:
        return self._entity.is_valid(self.name, self.version_major)

    def link_to_tool(self, tool: ToolID) -> None:
        if self._in_database() and self._entity.is_valid(tool.name, tool.version_major):
            self._client.sqlExec(
                f"""
                BEGIN TRANSACTION;
                INSERT INTO  entitylinker(system_name, system_major_version, tool_name, tool_major_version, valid, changed_at)
                VALUES ('{self.name}', {self.version_major}, '{tool.name}',{tool.version_major}, TRUE, NOW());
                COMMIT;
                 """
            )

    def remove_link_to_tool(self, tool: ToolID) -> None:
        if self._in_database() and self._entity.is_valid(tool.name, tool.version_major):
            self._client.sqlExec(
                f"""
                BEGIN TRANSACTION;
                INSERT INTO  entitylinker(system_name, tool_ownerversion_major, tool_name, toolversion_major, valid, changed_at)
                VALUES {self.name}, {self.version_major}, {tool.name}, {tool.version_major}, FALSE, NOW()
                COMMIT;
                 """
            )

    def get_linked_tools(self) -> List[ToolID]:
        valid_tools: List[ToolID] = []
        if self._in_database():
            tools_linked = self._client.sqlQuery(
                f"""
                SELECT linker.tool_name, linker.tool_major_version, tool.purpose
                FROM entitylinker AS linker
                INNER JOIN entity AS tool ON linker.tool_name = tool.name AND linker.tool_major_version = tool.version_major
                WHERE linker.system_name = '{self.name}' AND linker.system_major_version = {self.version_major} AND linker.valid = TRUE AND tool.is_system=FALSE;
                """
            )

            for (tool_name, tool_version, tool_purpose) in tools_linked:
                valid_tools.append(ToolID(name=tool_name, version_major=tool_version, purpose=tool_purpose))
        return valid_tools


class Tool:
    def __init__(self, client: ImmudbClient, name: str, version_major: int, purpose: str) -> None:
        self._client = client
        self._entity = DataBaseEntity(client=client)
        self.name = name
        self.version_major = version_major
        self.purpose = purpose

    def add(self) -> None:
        self._entity.insert(
            ToolID(
                name=self.name,
                version_major=self.version_major,
                purpose=self.purpose,
            )
        )

    def _in_database(self) -> bool:
        return self._entity.is_valid(self.name, self.version_major)

    def get_linked_systems(self) -> List[SystemID]:
        valid_systems: List[SystemID] = []
        if self._in_database():
            tools_linked = self._client.sqlQuery(
                f"""
                SELECT linker.system_name, linker.system_major_version, system.purpose
                FROM entitylinker AS linker
                INNER JOIN entity AS system ON linker.system_name = system.name AND linker.system_major_version = system.version_major
                WHERE linker.tool_name = '{self.name}' AND linker.tool_major_version = {self.version_major} AND valid = TRUE AND system.is_system=TRUE;
                """
            )
            for tool in tools_linked:
                (system_name, system_major_version, purpose) = tool
                valid_systems.append(
                    System(self._client, name=system_name, version_major=system_major_version, purpose=purpose)
                )
        return valid_systems
