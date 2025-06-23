from database_service.abcs.database_abc import DatabaseABC
from .abcs.database_service_abc import DatabaseServiceABC
from consistent_hash_service.service import ConsistentHashServiceSingleton, ConsistentHashService
from typing import TypeVar
from sqlalchemy.orm import DeclarativeBase

T = TypeVar('T', bound=DeclarativeBase)

class DatabaseService(DatabaseServiceABC):
    def __init__(self, schema, consistent_hash_service: ConsistentHashService | None = None):
        self.schema = schema
        self.consistent_hash_service = consistent_hash_service or ConsistentHashServiceSingleton()
    
    async def connect(self) -> None:
        databases: list[DatabaseABC] = await self.consistent_hash_service.get_all_database()
        for database in databases:
            await database.connect()
    
    async def disconnect(self) -> None:
        databases: list[DatabaseABC] = await self.consistent_hash_service.get_all_database()
        for database in databases:
            await database.disconnect()
    
    async def create_one(self, data, source_shard_id: str):
        database = await self.consistent_hash_service.get_database_from_unique_id(data.id)
        return await database.create_one(data, self.schema)
    
    async def update_one(self, id: str, data):
        database = await self.consistent_hash_service.get_database_from_unique_id(id)
        return await database.update_one(id, data, self.schema)
    
    async def get_one(self, id: str):
        database = await self.consistent_hash_service.get_database_from_unique_id(id)
        return database.get_one(id, self.schema)
    
    async def get_all(self, query) -> list:
        databases = await self.consistent_hash_service.get_all_database()
        result = []
        for database in databases:
            result.append(await database.get_all(query, self.schema))
        return result

    async def delete_one(self, id: str) -> None:
        database = await self.consistent_hash_service.get_database_from_unique_id(id)
        return await database.delete_one(id, self.schema)
    
    async def create_using_selected_database(self, data, database):
        return await database.create_one(data, self.schema)
    
    async def update_using_selected_database(self, id: str, data, database):
        return await database.update_one(id, data, self.schema)
    
    async def delete_using_selected_database(self, id: str, database: DatabaseABC):
        return await database.delete_one(id, self.schema)
    
    async def create_metadata(self):
        databases = await self.consistent_hash_service.get_all_database()
        for database in databases:
            await database.create_metadata(self.schema)
