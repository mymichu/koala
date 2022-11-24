from typing import List

from immudb import ImmudbClient

from koala.database.model import document as DocumentDB
from koala.database.model import link_docs_to_entity as LinkerDocEntityDB
from koala.database.model import link_ownership_to_entity as LinkerOwnershipEntityDB
from koala.database.model import link_system_to_tool as LinkerSystemToolDB
from koala.database.model import tool as ToolDB

from .types import Document, System, Tool


class ToolApi:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def _convert(self, tools: List[ToolDB.ToolID]) -> List[Tool]:
        return [Tool(tool.name, tool.version_major, tool.purpose, tool.identity, tool.gmp_relevant) for tool in tools]

    def get_gmp_relevant_tools(self) -> List[Tool]:
        monitor_database = ToolDB.ToolMonitor(self._client)
        tool_database = monitor_database.get_gmp_relevant_tools()
        return self._convert(tool_database)

    def get_non_gmp_relevant_tools(self) -> List[Tool]:
        monitor_database = ToolDB.ToolMonitor(self._client)
        tool_database = monitor_database.get_non_gmp_relevant_tools()
        return self._convert(tool_database)

    def get_all_gmp_relevant_tools(self) -> List[Tool]:
        pass

    def unlinked_tools(self) -> List[Tool]:
        monitor_database = ToolDB.ToolMonitor(self._client)
        tool_database = monitor_database.unlinked_tools()
        return self._convert(tool_database)

    def get_all_tools(self) -> List[Tool]:
        monitor_database = ToolDB.ToolMonitor(self._client)
        tool_database = monitor_database.get_all_tools()
        return self._convert(tool_database)

    def get_tools(self, name: str) -> List[Tool]:
        monitor_database = ToolDB.ToolMonitor(self._client)
        tool_database = monitor_database.get_tools(name)
        return self._convert(tool_database)

    def add_tool(self, tool: Tool) -> Tool:
        tool_database = ToolDB.Tool(self._client, tool.name, tool.version_major, tool.purpose, tool.gmp_relevant)
        tool_database.add()
        tool.identity = tool_database.get_id()
        return tool

    def link_tools_to_system(self, tools_id: List[int], system_id: int) -> None:
        for tool_id in tools_id:
            linker = LinkerSystemToolDB.LinkSystemTool(self._client, system_id, tool_id)
            linker.add()

    def add_tool_owner(self, tool: Tool, owner_email: str) -> None:
        entitiy = ToolDB.ToolID(tool.name, tool.version_major, tool.purpose)
        linker = LinkerOwnershipEntityDB.LinkOwnershipToEntity(self._client, entitiy, owner_email)
        linker.link()

    def get_all_tools_owned_by(self, owner_email: str) -> List[Tool]:
        list_tools = ToolDB.ToolMonitor(self._client).get_all_tools_owned_by(owner_email)
        return self._convert(list_tools)

    def get_tool_documents(self, tool: Tool) -> List[Document]:
        tool_db = ToolDB.Tool(self._client, tool.name, tool.version_major, tool.purpose, tool.gmp_relevant)
        tool_id = tool_db.get_id()

        doc_linker = LinkerDocEntityDB.LinkDocEntityMonitor(self._client)
        docs_db = doc_linker.get_linked_to_tools(tool_id)
        return [Document(doc_db.name, doc_db.path) for doc_db in docs_db]

    def add_tool_document(self, tool: Tool, document: Document) -> None:
        doc_db = DocumentDB.Document(self._client, document.name, document.path)
        document_id = doc_db.get_id()
        tool_db = ToolDB.Tool(self._client, tool.name, tool.version_major, tool.purpose, tool.gmp_relevant)
        tool_id = tool_db.get_id()

        link = LinkerDocEntityDB.LinkDocEntity(
            self._client,
            document_id,
            tool_id,
        )
        link.add()

    def get_systems_for_tool(self, tool_id: int) -> List[System]:
        system_tool_linker = LinkerSystemToolDB.LinkSystemToolMonitor(self._client)
        systems_database = system_tool_linker.get_linked_systems(tool_id)
        return [
            System(
                system_db.name,
                version_major=system_db.version_major,
                purpose=system_db.purpose,
                identity=system_db.identity,
            )
            for system_db in systems_database
        ]
