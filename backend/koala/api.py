from dataclasses import dataclass
from typing import Any, Dict, List

from immudb import ImmudbClient

from koala.database.model import document as DocumentDB
from koala.database.model import link_docs_to_entity, link_system_to_tool
from koala.database.model import system as SystemDB
from koala.database.model import tool as ToolDB
from koala.database.model.document import Document as DatabaseDocument
from koala.database.model.link_docs_to_entity import (
    LinkDocEntity as DatabaseLinkDocEntity,
)
from koala.database.model.link_system_to_tool import (
    LinkSystemTool as DatabaseLinkSystemTool,
)
from koala.database.model.system import System as DataBaseSystem
from koala.database.model.system import SystemID
from koala.database.model.tool import Tool as DatabaseTool
from koala.database.model.tool import ToolID
from koala.database.monitor import Monitor as DataBaseMonitor


@dataclass(unsafe_hash=True)
class Document:
    name: str
    path: str


@dataclass(unsafe_hash=True)
class LinkDocEntity:
    document_id: int
    entity_id: int


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

    def add_link_doc_entity(self, link: LinkDocEntity) -> None:
        link_database = DatabaseLinkDocEntity(self._client, link.document_id, link.entity_id)
        link_database.add()

    def get_link_doc_entity(self, **kwargs: Dict[str, Any]) -> List[LinkDocEntity]:
        return [
            LinkDocEntity(link.document_id, link.entity_id)
            for link in link_docs_to_entity.get_by(self._client, **kwargs)
        ]

    def add_system_document(self, system: System, document: Document) -> None:
        doc_db = DocumentDB.get_by(
            self._client,
            name=document.name,
            path=document.path,
        )
        sys_db = SystemDB.get_by(
            self._client,
            name=system.name,
            version_major=system.version_major,
            purpose=system.purpose,
        )

        if len(sys_db) != 1:
            raise Exception("Ambigious system")

        if len(doc_db) != 1:
            raise Exception("Ambigious document")

        link = DatabaseLinkDocEntity(
            self._client,
            doc_db[0].id,
            sys_db[0].id,
        )
        link.add()

    def get_system_documents(self, system: System) -> List[Document]:
        sys_db = SystemDB.get_by(
            self._client,
            name=system.name,
            version_major=system.version_major,
            purpose=system.purpose,
        )

        if len(sys_db) != 1:
            raise Exception("Ambigious system")

        docs_db = link_docs_to_entity.get_linked_to_systems(self._client, sys_db[0])

        return [Document(doc_db.name, doc_db.path) for doc_db in docs_db]

    def add_tool_document(self, tool: Tool, document: Document) -> None:
        doc_db = DocumentDB.get_by(
            self._client,
            name=document.name,
            path=document.path,
        )
        tool_db = ToolDB.get_by(
            self._client,
            name=tool.name,
            version_major=tool.version_major,
            purpose=tool.purpose,
        )

        if len(tool_db) != 1:
            raise Exception("Ambigious tool")

        if len(doc_db) != 1:
            raise Exception("Ambigious document")

        link = DatabaseLinkDocEntity(
            self._client,
            doc_db[0].id,
            tool_db[0].id,
        )
        link.add()

    def get_tool_documents(self, tool: Tool) -> List[Document]:
        tool_db = ToolDB.get_by(
            self._client,
            name=tool.name,
            version_major=tool.version_major,
            purpose=tool.purpose,
        )

        if len(tool_db) != 1:
            raise Exception("Ambigious tool")

        docs_db = link_docs_to_entity.get_linked_to_tools(self._client, tool_db[0])

        return [Document(doc_db.name, doc_db.path) for doc_db in docs_db]

    @staticmethod
    def _convert_to(target_type: Any, tool_database: Any) -> List[Any]:
        tools: List[Any] = []
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

    def get_tools_for_system(self, system: System) -> List[Tool]:
        system_db = DataBaseSystem(self._client, system.name, system.version_major, system.purpose)
        tool_database = link_system_to_tool.get_linked_tools(self._client, system_db)
        return self._convert_to(Tool, tool_database)

    def get_systems_for_tool(self, tool: Tool) -> List[System]:
        tool_db = DatabaseTool(self._client, tool.name, tool.version_major, tool.purpose)
        systems_database = link_system_to_tool.get_linked_systems(self._client, tool_db)
        return self._convert_to(System, systems_database)

    def link_tools_to_system(self, tools: List[Tool], system: System) -> None:
        system_db = DataBaseSystem(self._client, system.name, system.version_major, system.purpose)
        for tool in tools:
            tool_db = ToolID(tool.name, tool.version_major, tool.purpose)
            link = DatabaseLinkSystemTool(self._client, system_db, tool_db)
            link.add()
