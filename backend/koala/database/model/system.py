from typing import Any, List

from immudb import ImmudbClient

from .entity import DataBaseEntity, Entity


# All Systems are GMP relevant
# pylint: disable=too-many-arguments
class System(DataBaseEntity):
    def __init__(
        self, client: ImmudbClient, name: str = "", version_major: int = -1, purpose: str = "", identity: int = -1
    ) -> None:
        super().__init__(
            client=client,
            name=name,
            version_major=version_major,
            purpose=purpose,
            gmp_relevant=True,
            identity=identity,
            is_system=True,
        )
        self._client = client


class SystemMonitor:
    def __init__(self, client: ImmudbClient) -> None:
        self._client = client

    # The order of the columns matters: id, name, version_major, purpose, changed_at, gmp_relevant
    def _convert_query_system_id(self, resp: Any) -> List[Entity]:
        systems: List[Entity] = []
        for item in resp:
            (identiy, name, version_major, purpose, changed_at, gmp_relevant) = item
            system = Entity(
                name=name,
                version_major=version_major,
                purpose=purpose,
                change_at=changed_at,
                gmp_relevant=gmp_relevant,
                identity=identiy,
            )
            systems.append(system)
        return systems

    def get_all_systems(self) -> List[Entity]:
        resp = self._client.sqlQuery(
            """
        SELECT id, name, version_major, purpose, changed_at, gmp_relevant FROM entity WHERE is_system = TRUE;
        """
        )

        return self._convert_query_system_id(resp)

    def get_all_system_owned_by(self, user_id: int) -> List[Entity]:
        resp = self._client.sqlQuery(
            """
            SELECT entity.id, entity.name, entity.version_major, entity.purpose, entity.changed_at, entity.gmp_relevant
            FROM entity_ownership
            INNER JOIN entity ON entity_ownership.entity_id = entity.id
            WHERE  entity_ownership.owner_id = @user_id AND entity.is_system = TRUE;
            """,
            params={"user_id": user_id},
        )

        return self._convert_query_system_id(resp)
