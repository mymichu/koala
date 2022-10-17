from dataclasses import dataclass
from example.database.types import SystemId, ToolId
from immudb import ImmudbClient
from typing import List


@dataclass
class Entity:
    name: str
    version_major: int
    purpose: str
    is_system: bool


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


class Tool:
    def __init__(self, client, tool_id: ToolId) -> None:
        self._client = client
        self._entity = DataBaseEntity(client=client)
        self._id = tool_id

    def add_to_database(self, purpose: str) -> None:
        self._entity.insert(
            Entity(
                name=self._id.name,
                version_major=self._id.major,
                purpose=purpose,
                is_system=False,
            )
        )

    @property
    def tool_id(self):
        return self._id

    def _in_database(self) -> bool:
        return self._entity.is_valid(self._id.name, self._id.major)

    def get_linked_systems(self) -> List[SystemId]:
        valid_systems: List[SystemId] = []
        if self._in_database():
            tools_linked = self._client.sqlQuery(
                f"""
                SELECT tool_owner_name, tool_owner_major_version FROM entitylinker WHERE tool_name = '{self._id.name}' AND tool_major_version = {self._id.major} AND valid = TRUE;
                """
            )
            for tool in tools_linked:
                (tool_owner_name, tool_owner_major_version) = tool
                valid_systems.append(SystemId(name=tool_owner_name, major=tool_owner_major_version))
        return valid_systems


class System:
    def __init__(self, client, name: str, version_major: int) -> None:
        self._client = client
        self._entity = DataBaseEntity(client=client)
        self._name = name
        self._version_major = version_major

    def add(self, purpose: str) -> None:
        self._entity.insert(
            Entity(
                name=self._name,
                version_major=self._version_major,
                purpose=purpose,
                is_system=True,
            )
        )

    def _in_database(self) -> bool:
        return self._entity.is_valid(self._name, self._version_major)

    def link_to_tool(self, tool_id: ToolId) -> None:
        if self._in_database() and self._entity.is_valid(tool_id.name, tool_id.major):
            self._client.sqlExec(
                f"""
                BEGIN TRANSACTION;
                INSERT INTO  entitylinker(tool_owner_name, tool_owner_major_version, tool_name, tool_major_version, valid, changed_at)
                VALUES ('{self._name}', {self._version_major}, '{tool_id.name}',{tool_id.major}, TRUE, NOW());
                COMMIT;
                 """
            )

    def remove_link_to_tool(self, tool_id: ToolId) -> None:
        if self._in_database() and self._entity.is_valid(tool_id.name, tool_id.major):
            self._client.sqlExec(
                f"""
                BEGIN TRANSACTION;
                INSERT INTO  entitylinker(tool_owner_name, tool_owner_version_major, tool_name, tool_version_major, valid, changed_at)
                VALUES {self._name}, {self._version_major}, {tool_id.name},{tool_id.major}, FALSE, NOW()
                COMMIT;
                 """
            )

    def get_linked_tools(self) -> List[ToolId]:
        valid_tools: List[ToolId] = []
        if self._in_database():
            tools_linked = self._client.sqlQuery(
                f"""
                SELECT tool_name, tool_major_version FROM entitylinker WHERE tool_owner_name = '{self._name}' AND tool_owner_major_version = {self._version_major} AND valid = TRUE;
                """
            )
            for tool in tools_linked:
                (name, major_version) = tool
                valid_tools.append(ToolId(name=name, major=major_version))
        return valid_tools
