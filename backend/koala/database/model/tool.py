from typing import Any, List

from immudb import ImmudbClient

from .entity import DataBaseEntity, Entity


# pylint: disable=too-many-arguments
class Tool(DataBaseEntity):
    def __init__(
        self,
        client: ImmudbClient,
        name: str = "",
        version_major: int = -1,
        purpose: str = "",
        identity: int = -1,
        gmp_relevant: bool = True,
    ) -> None:
        super().__init__(
            client=client,
            name=name,
            version_major=version_major,
            purpose=purpose,
            gmp_relevant=gmp_relevant,
            identity=identity,
            is_system=False,
        )
        self._client = client


class ToolMonitor:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    def unlinked_tools(self) -> List[Entity]:
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
                unlinked_tools.append(Entity(name=name, version_major=version_major, purpose=purpose))

        return unlinked_tools

    # The order of the columns matters: id, name, version_major, purpose, changed_at, is_system, gmp_relevant
    def _convert_query_tool_id(self, resp: Any) -> List[Entity]:
        tools: List[Entity] = []
        for item in resp:
            (identiy, name, version_major, purpose, changed_at, is_system, gmp_relevant) = item
            tool = Entity(
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

    def get_all_tools(self) -> List[Entity]:
        resp = self._client.sqlQuery(
            """
        SELECT id, name, version_major, purpose, changed_at, is_system, gmp_relevant FROM entity WHERE is_system = FALSE;
        """
        )
        return self._convert_query_tool_id(resp)

    def get_tools(self, name: str) -> List[Entity]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose, gmp_relevant FROM entity
        WHERE name = @name AND is_system = FALSE;
        """,
            params={"name": name},
        )
        return list(map(lambda x: Entity(*x), resp))

    def get_gmp_relevant_tools(self) -> List[Entity]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity
        WHERE gmp_relevant = TRUE AND is_system = FALSE;
        """
        )
        return list(map(lambda x: Entity(*x), resp))

    def get_non_gmp_relevant_tools(self) -> List[Entity]:
        resp = self._client.sqlQuery(
            """
        SELECT name, version_major, purpose FROM entity
        WHERE gmp_relevant = FALSE AND is_system = FALSE;
        """
        )
        return list(map(lambda x: Entity(*x), resp))

    def get_all_tools_owned_by(self, user_id: int) -> List[Entity]:
        resp = self._client.sqlQuery(
            """
            SELECT entity.id, entity.name, entity.version_major, entity.purpose, entity.changed_at, entity.is_system, entity.gmp_relevant
            FROM entity_ownership
            INNER JOIN entity ON entity_ownership.entity_id = entity.id
            WHERE  entity_ownership.owner_id = @user_id AND entity.is_system = FALSE;
            """,
            params={"user_id": user_id},
        )

        return self._convert_query_tool_id(resp)
