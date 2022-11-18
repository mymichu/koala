from immudb import ImmudbClient

from koala.database.model import document as DocumentDB

from .types import Document


class DocumentApi:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def add_document(self, document: Document) -> None:
        document_database = DocumentDB.Document(self._client, document.name, document.path)
        document_database.add()
