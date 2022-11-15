from dataclasses import dataclass
from datetime import datetime
from typing import List
from immudb import ImmudbClient


@dataclass(unsafe_hash=True)
class DocumentID:
    name: str
    path: str
    creation_date: datetime = None
    id: int = 0


class Document(DocumentID):
    def __init__(self, client: ImmudbClient, name: str, path: str):
        super().__init__(name=name, path=path)
        self._client = client

    def add(self) -> None:
        self._client.sqlExec(
            f"""
        BEGIN TRANSACTION;
            INSERT INTO document (name, path, creation_date)
            VALUES ('{self.name}', '{self.path}', NOW());
        COMMIT;
        """
        )


def get_by(client: ImmudbClient, **kwargs) -> List[DocumentID]:
    query = "SELECT name, path, id FROM document"
    sep = " WHERE "

    for key, value in kwargs.items():
        if isinstance(value, str):
            condition = f"{sep}{key}='{value}'"
        else:
            condition = f"{sep}{key}={value}"

        sep = " AND "
        query += condition

    resp = client.sqlQuery(query)
    return [DocumentID(*item) for item in resp]
