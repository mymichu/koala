from typing import List

from immudb import ImmudbClient

from koala.database.model import change as ChangeDB

from .types import Change


class ChangeApi:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def _convert(self, changes: List[ChangeDB.ChangeID]) -> List[Change]:
        return [
            Change(change.entity_id, change.requester_id, change.reviewer_id, change.description, change.identity)
            for change in changes
        ]

    def add_change(self, change: Change) -> Change:
        change_database = ChangeDB.Change(
            self._client,
            entity_id=change.entity_id,
            requester_id=change.requester_id,
            reviewer_id=change.reviewer_id,
            description=change.description,
        )
        change_database.add()
        change.identity = change_database.get_id()
        return change

    def review_change(self, change_id: int, reviewer_id: int) -> None:
        monitor_database = ChangeDB.Change(self._client, identity=change_id)
        monitor_database.update_reviewer(reviewer_id)

    def get_all_changes(self) -> List[Change]:
        monitor_database = ChangeDB.Change(self._client)
        change_database = monitor_database.get_all_changes()
        return self._convert(change_database)

    def get_all_changes_open(self) -> List[Change]:
        monitor_database = ChangeDB.Change(self._client)
        change_database = monitor_database.get_all_changes_open()
        return self._convert(change_database)

    def update_reviewer(self, change_id: int, reviewer_id: int) -> None:
        monitor_database = ChangeDB.Change(self._client, identity=change_id)
        monitor_database.update_reviewer(reviewer_id)
