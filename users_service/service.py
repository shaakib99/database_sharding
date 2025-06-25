from .schema import UserSchema
from .models import CreateUserModel, UserModel, UpdateUserModel
from database_service.service import DatabaseService, DatabaseServiceABC
from database_service.unique_id_generator_service.service import IDGeneratorService
from database_service.models import QueryModel
class UsersService:
    def __init__(self, database_service: DatabaseServiceABC | None = None, id_generation_service: IDGeneratorService | None = None):
        self.schema = UserSchema
        self.database_service = database_service or DatabaseService(self.schema)
        self.id_generation_service = IDGeneratorService()

    async def create_one(self, data: CreateUserModel):
        model = UserModel()
        model.id = self.id_generation_service.generate('USER_')
        model.shard_id = model.id
        for key, value in data.model_dump().items():
            setattr(model, key, value)
        return await self.database_service.create_one(model, model.id)
    
    async def update_one(self, id: str, data: UpdateUserModel):
        model = UserModel()
        for key, value in data.model_dump().items():
            setattr(model, key, value)
            
        model.id = id
        return await self.database_service.update_one(id, model)

    async def get_one(self, id: str):
        return await self.database_service.get_one(id)

    async def get_all(self, query: QueryModel):
        return await self.database_service.get_all(query)
    
    async def delete_one(self, id: str):
        return await self.database_service.delete_one(id)
