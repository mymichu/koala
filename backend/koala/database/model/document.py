from dataclasses import dataclass
from datetime import datetime
from typing import Any, List

from immudb import ImmudbClient


@dataclass(unsafe_hash=True)
class DocumentID:
    name: str
    path: str
    creation_date: datetime = datetime.now()
    identity: int = 0


class Document(DocumentID):
    def __init__(self, client: ImmudbClient, name: str, path: str):
        super().__init__(name=name, path=path)
        self._client = client

    def add(self) -> None:
        self._client.sqlExec(
            """
        BEGIN TRANSACTION;
            INSERT INTO document (name, path, creation_date)
            VALUES (@name, @path, NOW());
        COMMIT;
        """,
            params={
                "name": self.name,
                "path": self.path,
            },
        )

    def get_id(self) -> int:
        resp = self._client.sqlQuery(
            f"""
            SELECT id FROM document
            WHERE name='{self.name}'
            AND path='{self.path}'
            """
        )
        if len(resp) != 1:
            raise Exception("Document not found")
        return int(resp[0][0])
