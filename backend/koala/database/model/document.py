from dataclasses import dataclass
from datetime import datetime

from immudb import ImmudbClient


@dataclass(unsafe_hash=True)
class DocumentID:
    name: str
    path: str
    creation_date: datetime = datetime.now()
    identity: int = -1
    is_released: bool = False


class Document(DocumentID):
    def __init__(
        self, client: ImmudbClient, name: str = "", path: str = "", identity=-1, released: bool = False
    ) -> None:
        super().__init__(name=name, path=path, identity=identity, is_released=released)
        self._client = client

    def add(self) -> None:
        self._check_name_path()
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

    def _check_name_path(self):
        if len(self.name) == 0:
            raise ValueError("Document name cannot be empty")
        if len(self.path) == 0:
            raise ValueError("Document path cannot be empty")

    def _check_id(self):
        if self.identity == -1:
            raise ValueError("Document ID not set")

    def get_id(self) -> int:
        self._check_name_path()
        resp = self._client.sqlQuery(
            """
            SELECT id FROM document
            WHERE name=@name
            AND path=@path
            """,
            params={"name": self.name, "path": self.path},
        )
        if len(resp) != 1:
            raise Exception("Document not found")
        self.identity = int(resp[0][0])
        return self.identity

    def update_release_status(self, is_released: bool) -> None:
        self._check_id()
        self._client.sqlExec(
            """
            BEGIN TRANSACTION;
                UPSERT INTO document (id, is_released, creation_date)
                VALUES (@id, @released, NOW());
            COMMIT;
            """,
            params={"id": self.identity, "released": is_released},
        )
        self.is_released = is_released

    def get_release_status(self) -> bool:
        self._check_id()
        resp = self._client.sqlQuery(
            """
            SELECT is_released FROM document
            WHERE id=@id
            """,
            params={"id": self.identity},
        )
        if len(resp) != 1:
            raise Exception("Document not found")
        self.is_released = bool(resp[0][0])
        return self.is_released
