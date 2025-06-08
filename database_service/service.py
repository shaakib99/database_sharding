from database_service.abc_classes import DatabaseABC
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from common import CommonQueryModel, get_databases
from hash_factory import HashFactorySingleton, HashFactory
from typing import Type, Generic, TypeVar
from .redis_service import RedisService, RedisServiceSingleton

T = TypeVar('T', bound=DeclarativeBase)

class DatabaseService(Generic[T]):
    def __init__(self, schema: Type[T], redis_service: RedisService | None = None, hash_factory: HashFactory | None = None):
        self.schema = schema
        self.hash_factory = hash_factory or HashFactorySingleton()
        self.databases = get_databases()
        self.redis_service = redis_service or RedisServiceSingleton()
    
    async def connect(self):
        for database in self.databases:
            await database.connect()

    async def disconnect(self):
        for database in self.databases:
            await database.disconnect()
    
    async def get_shard_key_from_id(self, id: str) -> str:
        shard_key = id
        while await self.redis_service.get_value(shard_key) != shard_key:
            shard_key = await self.redis_service.get_value(shard_key)
            if shard_key is None:
                raise ValueError(f"Shard key not found for id: {id}")
        return shard_key

    async def get_one(self, id: str) -> T:
        shard_key = await self.get_shard_key_from_id(id)
        database: DatabaseABC = self.hash_factory.get_database_by_key(shard_key)
        return await database.get_one(shard_key, self.schema)

    async def get_all(self, query: CommonQueryModel) -> list[T]:
        result = []
        for database in self.databases:
            result.extend(await database.get_all(query, self.schema))
        return result

    async def create_one(self, data: BaseModel) -> T:
        database: DatabaseABC = self.hash_factory.get_database_by_key('')
        return await database.create_one(data, self.schema)

    async def update_one(self, id: str, data: BaseModel) -> T:
        database: DatabaseABC = self.hash_factory.get_database_by_key(id)
        return await database.update_one(id, data, self.schema)

    async def delete_one(self, id: str) -> None:
        database: DatabaseABC = self.hash_factory.get_database_by_key(id)
        return await database.delete_one(id, self.schema)