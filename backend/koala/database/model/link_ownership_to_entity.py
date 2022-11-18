from immudb import ImmudbClient

from .entity import EntityKey


class LinkeOwnershipToEntity:
    def __init__(self, client: ImmudbClient):
        self._client = client

    def link(self, entity_key: EntityKey, owner_email: str) -> None:
        # TODO: Merge it to one query this is not supported with immudb
        respEntity = self._client.sqlQuery(
            """
            SELECT entity.id, user.email FROM entity 
            INNER JOIN user ON user.email = @owner_email
            WHERE entity.name = @entity_name AND entity.version_major = @entity_version_major AND entity.purpose = @entity_purpose""",
            params={
                "entity_name": entity_key.name,
                "entity_version_major": entity_key.version_major,
                "entity_purpose": entity_key.purpose,
                "owner_email": owner_email,
            },
        )
        (entityid, email) = respEntity[0]
        if email == owner_email:
            self._client.sqlExec(
                """
            BEGIN TRANSACTION;
            INSERT INTO entity_ownership(entity_id, owner_email)
            VALUES( @entity_id, @owner_email );
            COMMIT;
                """,
                params={
                    "entity_id": entityid,
                    "owner_email": owner_email,
                },
            )
