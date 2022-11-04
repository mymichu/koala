from typing import List
from dataclasses import dataclass


@dataclass
class System:
    name: str
    version_major: int
    purpose: str


class Api:
    def __init__(self, client) -> None:
        self._client = client

    def get_all_systems(self) -> List[System]:
        return []

    def add_system(self, system: System) -> None:
        pass
