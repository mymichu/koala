from dataclasses import dataclass
from typing import Any, List

from immudb import ImmudbClient

from .document import DocumentID


@dataclass(unsafe_hash=True)
class LinkDocEntityID:
    entity_id: int
    document_id: int
    identity: int = 0


class LinkDocEntity(LinkDocEntityID):
    def __init__(self, client: ImmudbClient, document_id: int, entity_id: int):
        super().__init__(document_id=document_id, entity_id=entity_id)
        self._client = client

    def add(self) -> None:
        self._client.sqlExec(
            """
        BEGIN TRANSACTION;
            INSERT INTO entity_x_document(document_id, entity_id, creation_date)
            VALUES (@document_id, @entity_id, NOW());
        COMMIT;
        """,
            params={
                "document_id": self.document_id,
                "entity_id": self.entity_id,
            },
        )


class LinkDocEntityMonitor:
    def __init__(self, client: ImmudbClient):
        self._client = client

    def get_by(self, **kwargs: Any) -> List[LinkDocEntityID]:
        query = "SELECT document_id, entity_id, id FROM entity_x_document"
        sep = " WHERE "

        for key, value in kwargs.items():
            if isinstance(value, str):
                condition = f"{sep}{key}='{value}'"
            else:
                condition = f"{sep}{key}={value}"

            sep = " AND "
            query += condition

        resp = self._client.sqlQuery(query)
        return [LinkDocEntityID(*item) for item in resp]

    def get_linked_to_systems(self, system_id: int) -> List[DocumentID]:
        docs_linked = self._client.sqlQuery(
            """
            SELECT doc.name, doc.path, doc.creation_date, doc.id FROM document as doc
            INNER JOIN entity_x_document as linker ON linker.document_id = doc.id
            WHERE linker.entity_id = @system_id
            """,
            params={
                "system_id": system_id,
            },
        )
        return [DocumentID(name, path, creation_date, id) for (name, path, creation_date, id) in docs_linked]

    def get_linked_to_tools(self, tool_id: int) -> List[DocumentID]:
        docs_linked = self._client.sqlQuery(
            """
            SELECT doc.name, doc.path, doc.creation_date, doc.id FROM document as doc
            INNER JOIN entity_x_document as linker ON linker.document_id = doc.id
            WHERE linker.entity_id = @tool_id
            """,
            params={
                "tool_id": tool_id,
            },
        )
        return [DocumentID(name, path, creation_date, id) for (name, path, creation_date, id) in docs_linked]
