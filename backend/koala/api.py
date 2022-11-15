from dataclasses import dataclass
from typing import Any, List, Union

from immudb import ImmudbClient

from koala.database.entity import System as DataBaseSystem
from koala.database.entity import SystemID
from koala.database.entity import Tool as DatabaseTool
from koala.database.entity import ToolID
from koala.database.monitor import Monitor as DataBaseMonitor
from koala.database.model import Document as DatabaseDocument
from koala.database.model import document, DocumentID


@dataclass(unsafe_hash=True)
class Document:
    name: str
    path: str


@dataclass(unsafe_hash=True)
class Entity:
    name: str
    version_major: int
    purpose: str


class System(Entity):
    pass


class Tool(Entity):
    gmp_relevant: bool = True

    def __init__(self, name: str, version_major: int, purpose: str, gmp_relevant: bool = True) -> None:
        super().__init__(name=name, version_major=version_major, purpose=purpose)
        self.gmp_relevant = gmp_relevant


class Api:
    def __init__(self, client: ImmudbClient) -> None:
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

    def add_document(self, document: Document) -> None:
        document_database = DatabaseDocument(self._client, document.name, document.path)
        document_database.add()

    def get_document(self, **kwargs) -> List[DocumentID]:
        return document.get_by(self._client, **kwargs)

    def add_system_document(self, system: System, document: Document) -> None:
        pass

    def get_system_documents(self, system: System) -> List[Document]:
        pass

    @staticmethod
    def _convert_to(target_type, tool_database: Union[List[ToolID], List[SystemID]]) -> List[Any]:
        tools: List[target_type] = []
        for tool_db in tool_database:
            if isinstance(tool_db, ToolID):
                tools.append(target_type(tool_db.name, tool_db.version_major, tool_db.purpose, tool_db.gmp_relevant))
            elif isinstance(tool_db, SystemID):
                tools.append(target_type(tool_db.name, tool_db.version_major, tool_db.purpose))
            else:
                pass
                # should panic ?

        return tools

    def get_gmp_relevant_tools(self) -> List[Tool]:
        monitor_database = DataBaseMonitor(self._client)
        tool_database = monitor_database.get_gmp_relevant_tools()
        return self._convert_to(Tool, tool_database)

    def get_non_gmp_relevant_tools(self) -> List[Tool]:
        monitor_database = DataBaseMonitor(self._client)
        tool_database = monitor_database.get_non_gmp_relevant_tools()
        return self._convert_to(Tool, tool_database)

    def get_all_gmp_relevant_tools(self) -> List[Tool]:
        pass

    def unlinked_tools(self) -> List[Tool]:
        monitor_database = DataBaseMonitor(self._client)
        tool_database = monitor_database.unlinked_tools()
        return self._convert_to(Tool, tool_database)

    def get_all_tools(self) -> List[Tool]:
        monitor_database = DataBaseMonitor(self._client)
        tool_database = monitor_database.get_all_tools()
        return self._convert_to(Tool, tool_database)

    def get_tools(self, name: str) -> List[Tool]:
        monitor_database = DataBaseMonitor(self._client)
        tool_database = monitor_database.get_tools(name)
        return self._convert_to(Tool, tool_database)

    def add_tool(self, tool: Tool) -> None:
        tool_database = DatabaseTool(self._client, tool.name, tool.version_major, tool.purpose, tool.gmp_relevant)
        tool_database.add()

    def add_tool_document(self, tool: Tool, document: Document) -> None:
        pass

    def get_tool_documents(self, tool: Tool) -> List[Document]:
        pass

    def get_tools_for_system(self, system: System) -> List[Tool]:
        system_db = DataBaseSystem(self._client, system.name, system.version_major, system.purpose)
        tool_database = system_db.get_linked_tools()
        return self._convert_to(Tool, tool_database)

    def get_systems_for_tool(self, tool: Tool) -> List[System]:
        tool_db = DatabaseTool(self._client, tool.name, tool.version_major, tool.purpose)
        systems_database = tool_db.get_linked_systems()
        return self._convert_to(System, systems_database)

    def link_tools_to_system(self, tools: List[Tool], system: System) -> None:
        system_db = DataBaseSystem(self._client, system.name, system.version_major, system.purpose)
        for tool in tools:
            system_db.link_to_tool(ToolID(tool.name, tool.version_major, tool.purpose))
