from immudb import ImmudbClient

from koala.database.model.user import User, UserData


class UserApi:
    def __init__(self, client: ImmudbClient) -> UserData:
        self._client = client

    def add_user(self, user: UserData) -> None:
        user_database = User(self._client, user)
        user_database.add()
        return UserData(user.name, user.first_name, user.email, user.active, user_database.get_id())
