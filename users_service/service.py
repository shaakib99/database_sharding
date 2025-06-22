from .schema import UserSchema
from .models import CreateUserModel, UserModel, UpdateUserModel
from database_service.service import DatabaseService, DatabaseServiceABC
from database_service.unique_id_generator_service.service import IDGeneratorService
from consistent_hash_service.service import ConsistentHashServiceSingleton, ConsistentHashService
from database_service.models import QueryModel
class UsersService:
    def __init__(self, database_service: DatabaseServiceABC | None = None, id_generation_service: IDGeneratorService | None = None, consistent_hash_service: ConsistentHashService | None = None ):
        self.schema = UserSchema
        self.database_service = database_service or DatabaseService(self.schema)
        self.id_generation_service = IDGeneratorService()
        self.consistent_hash_service = consistent_hash_service or ConsistentHashServiceSingleton()

    
    async def create_one(self, data: CreateUserModel):
        model = UserModel()
        model.id = self.id_generation_service.generate('USER_')
        for key, value in data.model_dump().items():
            setattr(model, key, value)
        
        database = await self.consistent_hash_service.get_database_from_unique_id(model.id)
        return await database.create_one(model, self.schema)
    
    async def update_one(self, id: str, data: UpdateUserModel):
        model = UserModel()
        for key, value in data.model_dump().items():
            setattr(model, key, value)
            
        model.id = id
        
        database = await self.consistent_hash_service.get_database_from_unique_id(model.id)
        return await database.update_one(id, model, self.schema)

    async def get_one(self, id: str):
        database = await self.consistent_hash_service.get_database_from_unique_id(id)
        return await database.get_one(id, self.schema)

    async def get_all(self, query: QueryModel):
        databases = await self.consistent_hash_service.get_all_database()
        result = []
        for database in databases:
            result.append(await database.get_all(query, self.schema))
        return result
    
    async def delete_one(self, id: str):
        database = await self.consistent_hash_service.get_database_from_unique_id(id)
        return await database.delete_one(id, self.schema)
