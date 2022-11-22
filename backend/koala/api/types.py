from dataclasses import dataclass


@dataclass()
class Document:
    name: str
    path: str
    identity: int = -1

    # exclude identity from equality
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Document):
            raise TypeError("Can only compare Document with Document")
        return self.name == other.name and self.path == other.path

    def __hash__(self) -> int:
        return hash((self.name, self.path))


@dataclass(unsafe_hash=True)
class LinkDocEntity:
    document_id: int
    entity_id: int


@dataclass(eq=True)
class Entity:
    name: str
    version_major: int
    purpose: str
    identity: int = -1

    # exclude identity from equality
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError("Can only compare Entity with Entity")
        return self.name == other.name and self.version_major == other.version_major and self.purpose == other.purpose

    def __hash__(self) -> int:
        return hash((self.name, self.version_major, self.purpose))


@dataclass(eq=False)
class System(Entity):
    pass


# pylint: disable=too-many-arguments
@dataclass(eq=False)
class Tool(Entity):
    def __init__(
        self, name: str, version_major: int, purpose: str, identity: int = -1, gmp_relevant: bool = True
    ) -> None:
        super().__init__(name=name, version_major=version_major, purpose=purpose, identity=identity)
        self.gmp_relevant = gmp_relevant
