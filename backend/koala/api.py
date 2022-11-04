from typing import List
from dataclasses import dataclass


@dataclass
class System:
    name: str
    version_major: int
    purpose: str


class Tool:
    pass


class Api:
    def __init__(self, client) -> None:
        self._client = client

    def get_all_systems(self) -> List[System]:
        return []

    def add_system(self, system: System) -> None:
        pass

    def get_all_tools(self) -> List[Tool]:
        return []

    def add_tool(self, tool: Tool) -> None:
        pass
