from dataclasses import dataclass
from datetime import datetime

from immudb import ImmudbClient


@dataclass
class ChangeID:
    identity: int
    entity_name: str
    entity_major_version: int
    requester_id: int
    reviewer_id: int
    description: str
    creation_date: datetime = datetime.now()

class Change(ChangeID):
    def __init__(self, client: ImmudbClient, identity: int = -1, entity_name: str = '', entity_major_version: str = '', requester_id: int = -1, reviewer_id: int = -1, description: str = '') -> None:
        super().__init__(identity, entity_name, entity_major_version, requester_id, reviewer_id, description)
        self._client = client

    def add(self) -> None:
        self._check_id()
        self._client.sqlExec(
            """
            BEGIN TRANSACTION;
                INSERT INTO document (entity_name, entity_major_version, creation_date, requester_id, reviewer_id, description)
                VALUES (@name, @version, NOW(), @q_id, @r_id, @desc);
            COMMIT;
            """,
            params={
                'name': self.entity_name,
                'version': self.entity_major_version,
                'q_id': self.requester_id,
                'r_id': self.reviewer_id,
                'desc': self.description,
            }
        )


    def _check_id(self) -> None:
        if self.requester_id == -1:
            raise ValueError("Requestor ID not set")

        if self.reviewer_id == -1:
            raise ValueError("Reviewer ID not set")

