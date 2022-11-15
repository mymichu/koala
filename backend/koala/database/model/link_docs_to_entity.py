from dataclasses import dataclass
from typing import Any, Dict, List
from immudb import ImmudbClient


@dataclass(unsafe_hash=True)
class LinkDocEntityID:
    entity_id: int
    document_id: int
    id: int = 0


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


def get_by(client: ImmudbClient, **kwargs: Dict[str, Any]) -> List[LinkDocEntityID]:
    query = "SELECT document_id, entity_id, id FROM entity_x_document WHERE"
    sep = " "

    for key, value in kwargs.items():
        if isinstance(value, str):
            condition = f"{sep}{key}='{value}'"
        else:
            condition = f"{sep}{key}={value}"

        sep = " AND "
        query += condition

    resp = client.sqlQuery(query)
    return [LinkDocEntityID(*item) for item in resp]
