from immudb import ImmudbClient


class LinkOwnershipToEntity:
    def __init__(self, client: ImmudbClient, entity_id: int, owner_id: int):
        self._client = client
        self._entity_id = entity_id
        self._owner_id = owner_id

    def link(self) -> None:
        response_entity = self._client.sqlQuery(
            """
            SELECT COUNT(*) FROM entity WHERE id=@entity_id;
            """,
            params={"entity_id": self._entity_id},
        )
        response_user = self._client.sqlQuery(
            """
            SELECT COUNT(*) FROM user WHERE id=@owner_id;
            """,
            params={"owner_id": self._owner_id},
        )

        if response_entity[0][0] != 1 or response_user[0][0] != 1:
            raise ValueError("Entity or User does not exist")

        self._client.sqlExec(
            """
        BEGIN TRANSACTION;
        INSERT INTO entity_ownership(entity_id, owner_id)
        VALUES( @entity_id, @owner_id );
        COMMIT;
            """,
            params={
                "entity_id": self._entity_id,
                "owner_id": self._owner_id,
            },
        )
