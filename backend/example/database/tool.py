from datetime import datetime, date
from dataclasses import asdict
from example.database.types import Tool


class DataBaseToolsInterface:
    def check_entry(self, Tool: Tool) -> bool:
        raise NotImplementedError()

    def insert_entry(self, Tool: Tool) -> None:
        raise NotImplementedError()

    def get_entries(self, start_date: date, end_date: date) -> list:
        raise NotImplementedError()


class DataBaseTools(DataBaseToolsInterface):
    def __init__(self) -> None:
        # TODO
        pass

    def check_entry(self, Tool: Tool) -> bool:
        # TODO
        return False

    def insert_entry(self, Tool: Tool) -> None:
        # TODO
        pass

    def get_entries(self, start_date: date, end_date: date) -> list:
        # TODO
        return list()


class DatabaseToolsMocks(DataBaseToolsInterface):
    _collection: list

    def __init__(self) -> None:
        self._collection = []

    def check_entry(self, Tool: Tool) -> bool:
        return Tool in self._collection

    def insert_entry(self, Tool: Tool) -> None:
        self._collection.append(Tool)

    def get_entries(self, start_date: date, end_date: date) -> list:
        return [Tool for Tool in self._collection if start_date <= Tool.Tooldate <= end_date]
