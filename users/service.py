from common import ServiceABC, CommonQueryModel, generate_id, get_database_by_shard_key
from users import UserModel, UserModelCreate, UserModelUpdate, UserSchema
from database_service import DatabaseABC, DatabaseService


class UsersService(ServiceABC[UserModelCreate, UserModelUpdate, UserModel, CommonQueryModel, UserModel, UserSchema]):
    def __init__(self, database_service = None) -> None:
        self.schema = UserSchema
        self.database_service = database_service or DatabaseService[UserSchema](self.schema)

    async def create(self, data: UserModelCreate):
        unique_id = generate_id('USER_')
        user_model = UserModel()
        user_model.id = unique_id
        return await self.database_service.create_one(user_model)

    async def update(self, id: str, data: UserModelUpdate):
        user_model = UserModel()
        return await self.database_service.update_one(id, user_model)

    async def get_one(self, id: str):
        user_model = UserModel()
        return await self.database_service.get_one(id)

    async def get_all(self, query: CommonQueryModel):
        return await self.database_service.get_all(query)

    async def delete(self, id: str):
        return await self.database_service.delete_one(id)