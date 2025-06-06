from database_service.abc_classes import DatabaseABC
from database_service.mysql_service import MySQLServiceSingleton
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from common import CommonQueryModel
from hash_factory import HashFactorySingleton, HashFactory
from typing import Type, Generic, TypeVar

T = TypeVar('T', bound=DeclarativeBase)

class DatabaseService(Generic[T]):
    def __init__(self, schema: Type[T], hash_factory: HashFactory | None = None):
        self.schema = schema
        self.hash_factory = hash_factory or HashFactorySingleton()
    
    async def get_dabases(self) -> list[DatabaseABC]:
        databases: list[DatabaseABC] = [
            MySQLServiceSingleton()
        ]
        return databases

    async def connect(self):
        databases: list[DatabaseABC] = [
            MySQLServiceSingleton()
        ]
        for database in databases:
            await database.connect()
    
    async def disconnect(self):
        databases: list[DatabaseABC] = [
            MySQLServiceSingleton()
        ]
        for database in databases:
            await database.disconnect()
    
    async def get_one(self, id: str, shard_key: str) -> T:
        database: DatabaseABC = self.hash_factory.get_database_by_key(id)
        return await database.get_one(id, self.schema)

    async def get_all(self, query: CommonQueryModel) -> list[T]:
        databases: list[DatabaseABC] = [
            MySQLServiceSingleton()
        ]
        result = []
        for database in databases:
            result.extend(await database.get_all(query, self.schema))
        return result

    async def create_one(self, data: BaseModel, shard_key: str) -> T:
        database: DatabaseABC = self.hash_factory.get_database_by_key(shard_key)
        return await database.create_one(data, self.schema)

    async def update_one(self, id: str, data: BaseModel, shard_key: str) -> T:
        database: DatabaseABC = self.hash_factory.get_database_by_key(id)
        return await database.update_one(id, data, self.schema)

    async def delete_one(self, id: str, shard_key: str) -> None:
        database: DatabaseABC = self.hash_factory.get_database_by_key(id)
        return await database.delete_one(id, self.schema)