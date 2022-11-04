from typing import List
from dataclasses import dataclass


@dataclass
class System:
    name: str
    version_major: int
    purpose: str


class Api:
    def __init__(self, client) -> None:
        pass

    def get_all_systems(self) -> List[System]:
        pass

    def add_system(self, system: System) -> None:
        pass
