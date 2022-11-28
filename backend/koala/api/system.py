from dataclasses import dataclass
from typing import List

from immudb import ImmudbClient

from koala.database.model import change as ChangeDB
from koala.database.model import document as DocumentDB
from koala.database.model import link_docs_to_entity as LinkerDocEntityDB
from koala.database.model import link_ownership_to_entity as LinkerOwnershipEntityDB
from koala.database.model import link_system_to_tool as LinkerSystemToolDB
from koala.database.model import system as SystemDB
from koala.database.model.link_docs_to_entity import (
    LinkDocEntity as DatabaseLinkDocEntity,
)

from .types import Document, System, Tool


@dataclass
# pylint: disable=too-many-instance-attributes
class SystemStatus:
    is_productive: bool
    amount_documents_released: int
    amount_documents_unreleased: int
    amount_tools_productive: int
    amount_tools_not_productive: int
    amount_systems_productive: int
    amount_systems_not_productive: int
    amount_change_request_closed: int
    amount_change_request_open: int


class SystemApi:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def _convert(self, systems: List[SystemDB.Entity]) -> List[System]:
        return [
            System(system.name, system.version_major, system.purpose, identity=system.identity) for system in systems
        ]

    def get_all_systems(self) -> List[System]:
        monitor_database = SystemDB.SystemMonitor(self._client)
        systems_database = monitor_database.get_all_systems()
        systems: List[System] = []
        for system_db in systems_database:
            systems.append(
                System(system_db.name, system_db.version_major, system_db.purpose, identity=system_db.identity)
            )
        return systems

    def add_system(self, system: System) -> System:
        system_database = SystemDB.System(self._client, system.name, system.version_major, system.purpose)
        system_database.add()
        return System(system.name, system.version_major, system.purpose, identity=system_database.get_id())

    def add_system_document(self, system_id: int, document: Document) -> None:
        document_id = DocumentDB.Document(self._client, document.name, document.path).get_id()

        link = DatabaseLinkDocEntity(
            self._client,
            document_id,
            system_id,
        )
        link.add()

    def get_tools_for_system(self, system_id: int) -> List[Tool]:
        system_to_tool_linker = LinkerSystemToolDB.LinkSystemToolMonitor(self._client)
        tool_database = system_to_tool_linker.get_linked_tools(system_id)
        return [Tool(tool.name, tool.version_major, tool.purpose, identity=tool.identity) for tool in tool_database]

    def get_system_documents(self, system_id: int) -> List[Document]:
        linker = LinkerDocEntityDB.LinkDocEntityMonitor(self._client)

        docs_db = linker.get_linked_to_systems(system_id)

        return [Document(doc_db.name, doc_db.path) for doc_db in docs_db]

    def get_system_status(self, system_id: int) -> SystemStatus:
        system = SystemDB.System(self._client, identity=system_id)
        linker = LinkerDocEntityDB.LinkDocEntityMonitor(self._client)
        changes = ChangeDB.Change(self._client)
        is_productive = system.is_active()
        released_docs = linker.get_amount_of_documents_of_entity(system_id, is_released=True)
        unreleased_docs = linker.get_amount_of_documents_of_entity(system_id, is_released=False)
        closed_change_requests = changes.get_amount_changes_reviewed(system_id)
        open_change_requests = changes.get_amount_changes_not_reviewed(system_id)

        return SystemStatus(
            is_productive=is_productive,
            amount_documents_released=released_docs,
            amount_documents_unreleased=unreleased_docs,
            amount_tools_productive=0,
            amount_tools_not_productive=0,
            amount_systems_productive=0,
            amount_systems_not_productive=0,
            amount_change_request_closed=closed_change_requests,
            amount_change_request_open=open_change_requests,
        )

    def set_system_productive(self, system_id: int) -> None:
        system = SystemDB.System(self._client, identity=system_id)
        system.set_active_status(True)

    def set_system_unproductive(self, system_id: int) -> None:
        system = SystemDB.System(self._client, identity=system_id)
        system.set_active_status(False)

    def add_system_owner(self, system_id: int, owner_id: int) -> None:
        LinkerOwnershipEntityDB.LinkOwnershipToEntity(self._client, system_id, owner_id).link()

    # TODO: move that to user api - is more logical
    def get_all_system_owned_by(self, owner_id: int) -> List[System]:
        list_tools = SystemDB.SystemMonitor(self._client).get_all_system_owned_by(owner_id)
        return self._convert(list_tools)
