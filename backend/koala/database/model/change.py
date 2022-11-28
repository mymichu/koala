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
    # pylint: disable=too-many-arguments
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

    # The order of the columns matters: id, entity_id, requester_id, reviewer_id, description, creation_date
    def _convert_query_change_id(self, resp: List[tuple]) -> List[ChangeID]:
        changes: List[ChangeID] = []
        for item in resp:
            (identity, entity_id, requester_id, reviewer_id, description, creation_date) = item
            change = ChangeID(
                identity=identity,
                entity_id=entity_id,
                requester_id=requester_id,
                reviewer_id=reviewer_id,
                description=description,
                creation_date=creation_date,
            )
            changes.append(change)
        return changes

    def add(self) -> None:
        self._check_entity(self.entity_id)
        self._check_user(self.requester_id)

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

    def get_data_by_id(self) -> ChangeID:
        resp = self._client.sqlQuery(
            """
            SELECT id, entity_id, requester_id, reviewer_id, description, creation_date FROM change
            WHERE id=@id;
            """,
            params={"id": self.identity},
        )
        data = self._convert_query_change_id(resp)[0]
        self.entity_id = data.entity_id
        self.requester_id = data.requester_id
        self.reviewer_id = data.reviewer_id
        self.description = data.description
        self.creation_date = data.creation_date
        return data

    def update_reviewer(self, reviewer_id: int) -> None:
        self._check_user(reviewer_id)
        self._check_id()
        # TODO: do we really need to query all of the data of a row only to update one value of a row
        self.get_data_by_id()
        self._client.sqlExec(
            """
            BEGIN TRANSACTION;
                UPSERT INTO change (id, entity_id, creation_date, requester_id, reviewer_id, description)
                VALUES (@id, @entity_id, @creation_date, @requester_id, @reviewer_id, @description);
            COMMIT;
            """,
            params={
                "id": self.identity,
                "entity_id": self.entity_id,
                "creation_date": self.creation_date,
                "requester_id": self.requester_id,
                "reviewer_id": reviewer_id,
                "description": self.description,
            },
        )
        self.reviewer_id = reviewer_id

    def _check_user(self, user_id: int) -> None:
        response_user = self._client.sqlQuery(
            """
            SELECT COUNT(*) FROM user WHERE id=@user_id;
            """,
            params={"user_id": user_id},
        )

        if response_user[0][0] != 1:
            raise ValueError("User does not exist")

    def _check_entity(self, entity_id: int) -> None:
        response_user = self._client.sqlQuery(
            """
            SELECT COUNT(*) FROM entity WHERE id=@entity_id;
            """,
            params={"entity_id": entity_id},
        )

        if response_user[0][0] != 1:
            raise ValueError("Entity does not exist")

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

    def _check_description(self) -> None:
        if len(self.description) > 0:
            raise ValueError("Description need to be set")

    def _check_id(self) -> None:
        if self.identity == -1:
            raise ValueError("Change identity not set")

    def get_all_changes(self) -> List[ChangeID]:
        resp = self._client.sqlQuery(
            """
            SELECT id, entity_id, requester_id, reviewer_id, description, creation_date FROM change;
            """
        )
        return self._convert_query_change_id(resp)

    def get_all_changes_open(self) -> List[ChangeID]:
        resp = self._client.sqlQuery(
            """
            SELECT id, entity_id, requester_id, reviewer_id, description, creation_date FROM change
            WHERE reviewer_id=-1;
            """
        )
        return self._convert_query_change_id(resp)

    def get_amount_changes_not_reviewed(self, entity_id: int) -> int:
        resp = self._client.sqlQuery(
            """
            SELECT COUNT(*) FROM change
            INNER JOIN entity ON change.entity_id=entity.id
            WHERE entity_id=@e_id AND reviewer_id=-1;
            """,
            params={"e_id": entity_id},
        )
        return int(resp[0][0])

    def get_amount_changes_reviewed(self, entity_id: int) -> int:
        resp = self._client.sqlQuery(
            """
            SELECT COUNT(*) FROM change
            WHERE (entity_id=@e_id AND reviewer_id > -1);
            """,
            params={"e_id": entity_id},
        )
        return int(resp[0][0])
