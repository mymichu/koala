from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Document:
    name: str
    path: str


@dataclass(unsafe_hash=True)
class LinkDocEntity:
    document_id: int
    entity_id: int


@dataclass(unsafe_hash=True)
class Entity:
    name: str
    version_major: int
    purpose: str


class System(Entity):
    pass


class Tool(Entity):
    def __init__(self, name: str, version_major: int, purpose: str, gmp_relevant: bool = True) -> None:
        super().__init__(name=name, version_major=version_major, purpose=purpose)
        self.gmp_relevant = gmp_relevant
