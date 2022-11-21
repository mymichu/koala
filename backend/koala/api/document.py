from immudb import ImmudbClient

from koala.database.model import document as DocumentDB

from .types import Document


class DocumentApi:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def add_document(self, document: Document) -> Document:
        document_database = DocumentDB.Document(self._client, document.name, document.path)
        document_database.add()
        return Document(document.name, document.path, identity=document_database.get_id())

    def update_release_status(self, document_id: int, release_status: bool) -> None:
        document_database = DocumentDB.Document(self._client, identity=document_id)
        document_database.update_release_status(release_status)

    def get_release_status(self, document_id: int) -> bool:
        document_database = DocumentDB.Document(self._client, identity=document_id)
        return document_database.get_release_status()
