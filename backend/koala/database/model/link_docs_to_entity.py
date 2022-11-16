from dataclasses import dataclass
from typing import Any, List

from immudb import ImmudbClient

from .document import DocumentID
from .system import SystemID
from .tool import ToolID


@dataclass(unsafe_hash=True)
class LinkDocEntityID:
    entity_id: int
    document_id: int
    _id: int = 0



class LinkDocEntity(LinkDocEntityID):
    def __init__(self, client: ImmudbClient, document_id: int, entity_id: int):
        super().__init__(document_id=document_id, entity_id=entity_id)
        self._client = client

    def add(self) -> None:
        self._client.sqlExec(
            f"""
        BEGIN TRANSACTION;
            INSERT INTO entity_x_document(document_id, entity_id, creation_date)
            VALUES ({self.document_id}, {self.entity_id}, NOW());
        COMMIT;
        """
        )


def get_by(client: ImmudbClient, **kwargs: Any) -> List[LinkDocEntityID]:
    query = "SELECT document_id, entity_id, id FROM entity_x_document"
    sep = " WHERE "

    for key, value in kwargs.items():
        if isinstance(value, str):
            condition = f"{sep}{key}='{value}'"
        else:
            condition = f"{sep}{key}={value}"

        sep = " AND "
        query += condition

    resp = client.sqlQuery(query)
    return [LinkDocEntityID(*item) for item in resp]


def get_linked_to_systems(client: ImmudbClient, system: SystemID) -> List[DocumentID]:
    docs_linked = client.sqlQuery(
        f"""
        SELECT doc.name, doc.path, doc.creation_date, doc.id FROM document as doc
        INNER JOIN entity_x_document as linker ON linker.document_id = doc.id
        WHERE linker.entity_id = {system.id}
        """
    )
    return [DocumentID(name, path, creation_date, id) for (name, path, creation_date, id) in docs_linked]


def get_linked_to_tools(client: ImmudbClient, tool: ToolID) -> List[DocumentID]:
    docs_linked = client.sqlQuery(
        f"""
        SELECT doc.name, doc.path, doc.creation_date, doc.id FROM document as doc
        INNER JOIN entity_x_document as linker ON linker.document_id = doc.id
        WHERE linker.entity_id = {tool.id}
        """
    )
    return [DocumentID(name, path, creation_date, id) for (name, path, creation_date, id) in docs_linked]
