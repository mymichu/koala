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


def get_by(client: ImmudbClient, **kwargs: Any) -> List[DocumentID]:
    query = "SELECT name, path, creation_date, id FROM document"
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
