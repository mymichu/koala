from dataclasses import dataclass


@dataclass
class ToolId:
    name: str
    major: int


@dataclass
class SystemId:
    name: str
    major: int
