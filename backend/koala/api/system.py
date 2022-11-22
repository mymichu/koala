from typing import List

from immudb import ImmudbClient

from koala.database.model import document as DocumentDB
from koala.database.model import link_docs_to_entity as LinkerDocEntityDB
from koala.database.model import link_system_to_tool as LinkerSystemTool
from koala.database.model import system as SystemDB
from koala.database.model import tool as ToolDB
from koala.database.model.link_docs_to_entity import (
    LinkDocEntity as DatabaseLinkDocEntity,
)

from .types import Document, System


class SystemApi:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def _convert(self, systems: List[SystemDB.SystemID]) -> List[System]:
        return [
            System(system.name, system.version_major, system.purpose, identity=system.identity) for system in systems
        ]

    def get_all_systems(self) -> List[System]:
        monitor_database = SystemDB.SystemMonitor(self._client)
        systems_database = monitor_database.get_all_systems()
        systems: List[System] = []
        for system_db in systems_database:
            print(system_db)
            systems.append(
                System(system_db.name, system_db.version_major, system_db.purpose, identity=system_db.identity)
            )
        return systems

    def add_system(self, system: System) -> System:
        system_database = SystemDB.System(self._client, system.name, system.version_major, system.purpose)
        system_database.add()
        return System(system.name, system.version_major, system.purpose, identity=system_database.get_id())

    def add_system_document(self, system: System, document: Document) -> None:
        document_id = DocumentDB.Document(self._client, document.name, document.path).get_id()
        system_db_id = SystemDB.System(self._client, system.name, system.version_major, system.purpose).get_id()

        link = DatabaseLinkDocEntity(
            self._client,
            document_id,
            system_db_id,
        )
        link.add()

    def get_systems_for_tool(self, tool: ToolDB.Tool) -> List[System]:
        tool_db = ToolDB.Tool(self._client, tool.name, tool.version_major, tool.purpose)
        system_tool_linker = LinkerSystemTool.LinkSystemToolMonitor(self._client)
        systems_database = system_tool_linker.get_linked_systems(tool_db)
        return self._convert(systems_database)

    def get_system_documents(self, system_id: int) -> List[Document]:
        linker = LinkerDocEntityDB.LinkDocEntityMonitor(self._client)

        docs_db = linker.get_linked_to_systems(system_id)

        return [Document(doc_db.name, doc_db.path) for doc_db in docs_db]

    def get_system_status(self, system: System) -> str:
        system_db = SystemDB.System(self._client, system.name, system.version_major, system.purpose)
        documents = system_db.get_system_document_status()
        change_tickets = system_db.get_system_change_ticket_status()
        tools = system_db.get_all_tools()
        return system_db.get_status()
