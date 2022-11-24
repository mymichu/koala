from typing import List
from immudb import ImmudbClient

from koala.database.model import change as ChangeDB
from .types import Change


class ChangeApi:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def _convert(self, changes: List[ChangeDB.ChangeID]) -> List[Change]:
        return [Change(change.entity_id, change.requester_id, change.reviewer_id, change.description, change.identity) for change in changes]

    def add_change(self, change: Change) -> None:
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


    def get_all_changes(self) -> List[Change]:
        monitor_database = ChangeDB.Change(self._client)
        tool_database = monitor_database.get_all_changes()
        return self._convert(tool_database)