from ast import alias
from typing import List
from dataclasses import dataclass
from koala.database.entity import Tool as DatabaseTool, ToolID
from koala.database.entity import System as DataBaseSystem
from koala.database.monitor import Monitor as DataBaseMonitor


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
        monitor_database = DataBaseMonitor(self._client)
        systems_database = monitor_database.get_all_systems()
        systems: List[System] = []
        for system_db in systems_database:
            print(system_db)
            systems.append(System(system_db.name, system_db.version_major, system_db.purpose))
        return systems

    def add_system(self, system: System) -> None:
        system_database = DataBaseSystem(self._client, system.name, system.version_major, system.purpose)
        system_database.add()

    def get_all_tools(self) -> List[Tool]:
        monitor_database = DataBaseMonitor(self._client)
        tool_database = monitor_database.get_all_tools()
        tools: List[Tool] = []
        for tool_db in tool_database:
            print(tool_db)
            tools.append(Tool(tool_db.name, tool_db.version_major, tool_db.purpose))
        return tools

    def add_tool(self, tool: Tool) -> None:
        tool_database = DatabaseTool(self._client, tool.name, tool.version_major, tool.purpose)
        tool_database.add()

    def get_tools_for_system(self, system: System) -> List[Tool]:
        system_db = DataBaseSystem(self._client, system.name, system.version_major, system.purpose)
        tools = map(lambda tool: Tool(tool.name, tool.version_major, tool.purpose), system_db.get_linked_tools())
        return list(tools)

    def link_tools_to_system(self, tools: List[Tool], system: System) -> None:
        system_db = DataBaseSystem(self._client, system.name, system.version_major, system.purpose)
        for tool in tools:
            system_db.link_to_tool(ToolID(tool.name, tool.version_major, tool.purpose))
