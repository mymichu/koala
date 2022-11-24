from dataclasses import dataclass
from datetime import datetime
from typing import List

from immudb import ImmudbClient


@dataclass
class ChangeID:
    identity: int
    entity_id: int
    requester_id: int
    reviewer_id: int
    description: str
    creation_date: datetime = datetime.now()


class Change(ChangeID):
    def __init__(
        self,
        client: ImmudbClient,
        identity: int = -1,
        entity_id: int = -1,
        requester_id: int = -1,
        reviewer_id: int = -1,
        description: str = "",
    ) -> None:
        super().__init__(identity, entity_id, requester_id, reviewer_id, description)
        self._client = client

    def _convert_query_change_id(self, resp: tuple) -> List[ChangeID]:
        return [ChangeID(*item) for item in resp]

    def add(self) -> None:
        self._check_id()
        self._client.sqlExec(
            """
            BEGIN TRANSACTION;
                INSERT INTO change(entity_id, creation_date, requester_id, reviewer_id, description)
                VALUES (@e_id, NOW(), @q_id, @r_id, @desc);
            COMMIT;
            """,
            params={
                "e_id": self.entity_id,
                "q_id": self.requester_id,
                "r_id": self.reviewer_id,
                "desc": self.description,
            },
        )

    def get_id(self) -> int:
        resp = self._client.sqlQuery(
            """
            SELECT id FROM change
            WHERE entity_id=@e_id
            """,
            params={"e_id": self.entity_id},
        )

        if len(resp) != 1:
            raise Exception("Document not found")

        self.identity = int(resp[0][0])
        return self.identity

    def _check_id(self) -> None:
        if self.requester_id == -1:
            raise ValueError("Requestor ID not set")

    def get_all_changes(self) -> List[ChangeID]:
        resp = self._client.sqlQuery(
            """
            SELECT id, entity_id, requester_id, reviewer_id, description, creation_date FROM change;
            """
        )
        return self._convert_query_change_id(resp)
