from immudb import ImmudbClient

from .entity import EntityKey


class LinkOwnershipToEntity:
    def __init__(self, client: ImmudbClient, entity_key: EntityKey, owner_email: str):
        self._client = client
        self._entity_key = entity_key
        self._owner_email = owner_email

    def link(self) -> None:
        # TODO: Merge it to one query this is not supported with immudb
        resp_entity = self._client.sqlQuery(
            """
            SELECT entity.id, user.email FROM entity
            INNER JOIN user ON user.email = @owner_email
            WHERE entity.name = @entity_name AND entity.version_major = @entity_version_major AND entity.purpose = @entity_purpose""",
            params={
                "entity_name": self._entity_key.name,
                "entity_version_major": self._entity_key.version_major,
                "entity_purpose": self._entity_key.purpose,
                "owner_email": self._owner_email,
            },
        )
        (entityid, email) = resp_entity[0]
        if email == self._owner_email:
            self._client.sqlExec(
                """
            BEGIN TRANSACTION;
            INSERT INTO entity_ownership(entity_id, owner_email)
            VALUES( @entity_id, @owner_email );
            COMMIT;
                """,
                params={
                    "entity_id": entityid,
                    "owner_email": self._owner_email,
                },
            )
