from ast import alias
from typing import List
from dataclasses import dataclass
from koala.database.tool import Tool as DatabaseTool, System as DataBaseSystem


@dataclass(unsafe_hash=True)
class Entity:
    name: str
    version_major: int
    purpose: str


class System(Entity):
    pass


class Tool(Entity):
    pass


class Api:
    def __init__(self, client) -> None:
        self._client = client

    def get_all_systems(self) -> List[System]:
        return []

    def add_system(self, system: System) -> None:
        system_database = DataBaseSystem(self._client, system.name, system.version_major)
        system_database.add(system.purpose)

    def get_all_tools(self) -> List[Tool]:
        return []

    def add_tool(self, tool: Tool) -> None:
        pass

    def get_tools_for_system(self, system: System) -> List[Tool]:
        return []

    def link_tools_to_system(self, tools: List[Tool], system: System) -> None:
        pass
