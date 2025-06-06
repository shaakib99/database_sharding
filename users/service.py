from common import ServiceABC, CommonQueryModel
from users import UserModel, UserModelCreate, UserModelUpdate

class UsersService(ServiceABC[UserModelCreate, UserModelUpdate, UserModel, CommonQueryModel, UserModel]):
    def __init__(self) -> None:
        pass

    async def create(self, data: UserModelCreate) -> UserModel:
        user_model = UserModel()
        return user_model

    async def update(self, id: str, data: UserModelUpdate) -> UserModel:
        user_model = UserModel()
        return user_model

    async def get_one(self, id: str) -> UserModel:
        user_model = UserModel()
        return user_model

    async def get_all(self, query: CommonQueryModel) -> list[UserModel]:
        user_model = UserModel()
        return [user_model]

    async def delete(self, id: str) -> None:
        return None