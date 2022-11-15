from dataclasses import dataclass
from typing import Any, Dict, List
from immudb import ImmudbClient


@dataclass(unsafe_hash=True)
class DocumentID:
    name: str
    path: str
    id: int = 0

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, DocumentID):
            return NotImplemented
        return self.name == __o.name and self.path == __o.path


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


def get_by(client: ImmudbClient, **kwargs: Dict[str, Any]) -> List[DocumentID]:
    query = "SELECT name, path, id FROM document WHERE"
    sep = " "

    for key, value in kwargs.items():
        if isinstance(value, str):
            condition = f"{sep}{key}='{value}'"
        else:
            condition = f"{sep}{key}={value}"

        sep = " AND "
        query += condition

    resp = client.sqlQuery(query)
    return [DocumentID(*item) for item in resp]
