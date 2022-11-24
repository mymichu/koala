from pydoc import describe
from immudb import ImmudbClient

from koala.database.model import change as ChangeDB


from .types import Change

class UserApi:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def add_user(self, change: Change) -> None:
        change_database = ChangeDB.Change(self._client,
        entity_name=change.entity_name,
        entity_major_version=change.entity_major_version,
        requester_id=change.requester_id,
        reviewer_id=change.reviewer_id,
        description=change.description)
        change_database.add()
        change.identity = change_database.get_id()
        return change