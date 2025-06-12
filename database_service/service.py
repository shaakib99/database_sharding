from database_service.abc_classes import DatabaseABC
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from common import CommonQueryModel, get_databases
from typing import Type, Generic, TypeVar
from shard_service import ShardService, ShardServiceSingleton

T = TypeVar('T', bound=DeclarativeBase)

class DatabaseService(Generic[T]):
    def __init__(self, schema: Type[T], shard_service: ShardService | None = None):
        self.schema = schema
        self.databases = get_databases()
        self.shard_service = shard_service or ShardServiceSingleton()

    async def connect(self):
        for database in self.databases:
            await database.connect()

    async def disconnect(self):
        for database in self.databases:
            await database.disconnect()


    async def get_one(self, id: str) -> T:
        database: DatabaseABC = await self.shard_service.get_database_from_id(id)
        return await database.get_one(id, self.schema)

    async def get_all(self, query: CommonQueryModel) -> list[T]:
        result = []
        for database in self.databases:
            result.extend(await database.get_all(query, self.schema))
        return result

    async def create_one(self, data: BaseModel, shard_id: str) -> T:
        database: DatabaseABC = await self.shard_service.get_database_from_id(shard_id)
        result = await database.create_one(data, self.schema)
        await self.shard_service.add_id_to_shard(result.id, shard_id)
        return result

    async def update_one(self, id: str, data: BaseModel) -> T:
        database: DatabaseABC = await self.shard_service.get_database_from_id(id)
        return await database.update_one(id, data, self.schema)

    async def delete_one(self, id: str) -> None:
        database: DatabaseABC = await self.shard_service.get_database_from_id(id)
        return await database.delete_one(id, self.schema)