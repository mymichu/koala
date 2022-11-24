from pydantic import BaseModel


class Entitiy(BaseModel):
    name: str
    purpose: str
    version_major: int


class System(Entitiy):
    pass


class SystemExtended(System):
    identity: int


class Document(BaseModel):
    name: str
    path: str


class DocumentExtended(Document):
    name: str
    path: str
    identity: int


class Tool(Entitiy):
    gmp_relevant: bool


class ToolExtended(Tool):
    identity: int
