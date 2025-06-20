from .schema import UserSchema
from .models import CreateUserModel, UserModel
from database_service.service import DatabaseService, DatabaseServiceABC
from database_service.unique_id_generator_service.service import IDGeneratorService
from consistent_hash_service.service import ConsistentHashServiceSingleton, ConsistentHashService
class UsersService:
    def __init__(self, database_service: DatabaseServiceABC | None = None, id_generation_service: IDGeneratorService | None = None, consistent_hash_service: ConsistentHashService | None = None ):
        self.schema = UserSchema
        self.database_service = database_service or DatabaseService(self.schema)
        self.id_generation_service = IDGeneratorService()
        self.consistent_hash_service = consistent_hash_service or ConsistentHashService()

    
    async def create_one(self, data: CreateUserModel):
        model = UserModel()
        model.id = self.id_generation_service.generate('test', 'USER_')
        for key, value in data.model_dump().items():
            setattr(model, key, value)
        
        database = await self.consistent_hash_service.get_database_from_unique_id(model.id)
        return await database.create_one(model, self.schema)
