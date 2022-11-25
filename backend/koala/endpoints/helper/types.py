from typing import List

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


class Ownership(BaseModel):
    systems: List[SystemExtended] = []
    tools: List[ToolExtended] = []


class User(BaseModel):
    name: str
    first_name: str
    email: str


class UserExtended(User):
    active: bool = True
    identity: int = -1
    ownership: Ownership = Ownership()
