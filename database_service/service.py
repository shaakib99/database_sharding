from database_service.abc_classes import DatabaseABC
from database_service.mysql_service import MySQLServiceSingleton
from sqlalchemy.ext.declarative import DeclarativeMeta
from pydantic import BaseModel
from common import CommonQueryModel
from hash_factory import HashFactory

class DatabaseService:
    def __init__(self, schema: DeclarativeMeta):
        self.schema = schema
        self.hash_factory = HashFactory()

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
    
    async def get_one(self, id: str):
        database: DatabaseABC = self.hash_factory.get_db_by_key(id)
        return await database.get_one(id, self.schema)
    
    async def get_all(self, query: CommonQueryModel):
        databases: list[DatabaseABC] = [
            MySQLServiceSingleton()
        ]
        result = []
        for database in databases:
            result.extend(await database.get_all(query, self.schema))
        return result
    
    async def create_one(self, data: BaseModel):
        id: str = 'test' # This should be replaced with a real ID generation logic.
        database: DatabaseABC = self.hash_factory.get_db_by_key(id)
        return await database.create_one(data, self.schema)
    
    async def update_one(self, id: str, data: BaseModel):
        database: DatabaseABC = self.hash_factory.get_db_by_key(id)
        return await database.update_one(id, data, self.schema)
    
    async def delete_one(self, id: str):
        database: DatabaseABC = self.hash_factory.get_db_by_key(id)
        return await database.delete_one(id, self.schema)