from dataclasses import dataclass
from typing import Any, List

from immudb import ImmudbClient

from .entity import DataBaseEntity, Entity


@dataclass
class ToolID(Entity):
    is_system: bool = False


# pylint: disable=too-many-arguments
class Tool(ToolID):
    def __init__(
        self, client: ImmudbClient, name: str, version_major: int, purpose: str, gmp_relevant: bool = True
    ) -> None:
        super().__init__(name=name, version_major=version_major, purpose=purpose, gmp_relevant=gmp_relevant)
        self._client = client
        self._entity = DataBaseEntity(
            client=client,
            entity=ToolID(
                name=name,
                version_major=version_major,
                purpose=purpose,
                gmp_relevant=gmp_relevant,
            ),
        )

    def add(self) -> None:
        self._entity.insert()

    def get_id(self) -> int:
        return self._entity.get_id()


class ToolMonitor:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def unlinked_tools(self) -> List[ToolID]:
        # TODO: This should be done by database with
        # SELECT name, version_major, purpose FROM entity
        # WHERE is_system = FALSE
        # AND name NOT IN (SELECT tool_name FROM entitylinker);

        all_linked_tools = self._client.sqlQuery(
            """
            SELECT system_tool_id AS system_tool_id FROM entitylinker;
            """
        )
        all_linked_tools_list: List[int] = list(map(lambda x: int(x[0]), all_linked_tools))
        tools = self._client.sqlQuery(
            """
        SELECT id, name, version_major, purpose FROM entity
        WHERE is_system = FALSE;
        """,
        )
        unlinked_tools = []
        for tool in tools:
            (tool_id, name, version_major, purpose) = tool
            if tool_id not in all_linked_tools_list:
                print(tool_id)
                unlinked_tools.append(ToolID(name=name, version_major=version_major, purpose=purpose))

        return unlinked_tools

    # The order of the columns matters: id, name, version_major, purpose, changed_at, is_system, gmp_relevant
    def _convert_query_tool_id(self, resp: Any) -> List[ToolID]:
        tools: List[ToolID] = []
        for item in resp:
            (identiy, name, version_major, purpose, changed_at, is_system, gmp_relevant) = item
            tool = ToolID(
                name=name,
                version_major=version_major,
                purpose=purpose,
                is_system=is_system,
                gmp_relevant=gmp_relevant,
                change_at=changed_at,
                identity=identiy,
            )
            tools.append(tool)
        return tools

    def get_all_tools(self) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT id, name, version_major, purpose, changed_at, is_system, gmp_relevant FROM entity WHERE is_system = FALSE;
        """
        )
        return self._convert_query_tool_id(resp)

    def get_tools(self, name: str) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose, gmp_relevant FROM entity
        WHERE name = @name AND is_system = FALSE;
        """,
            params={"name": name},
        )
        return list(map(lambda x: ToolID(*x), resp))

    def get_gmp_relevant_tools(self) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity
        WHERE gmp_relevant = TRUE AND is_system = FALSE;
        """
        )
        return list(map(lambda x: ToolID(*x), resp))

    def get_non_gmp_relevant_tools(self) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity
        WHERE gmp_relevant = FALSE AND is_system = FALSE;
        """
        )
        return list(map(lambda x: ToolID(*x), resp))

    def get_all_tools_owned_by(self, email: str) -> List[ToolID]:
        resp = self._client.sqlQuery(
            """
            SELECT entity.id, entity.name, entity.version_major, entity.purpose, entity.changed_at, entity.is_system, entity.gmp_relevant
            FROM entity_ownership
            INNER JOIN entity ON entity_ownership.entity_id = entity.id
            WHERE  entity_ownership.owner_email = @user_email;
            """,
            params={"user_email": email},
        )

        return self._convert_query_tool_id(resp)
