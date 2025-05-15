from database_service.abc_classes import DatabaseABC
from database_service.mysql_service import MySQLServiceSingleton
from sqlalchemy.ext.declarative import DeclarativeMeta

class DatabaseService:
    def __init__(self, database: DatabaseABC, schema: DeclarativeMeta):
        self.database = database or MySQLServiceSingleton()
        self.schema = schema

    async def connect(self):
        await self.database.connect()
    
    async def disconnect(self):
        await self.database.disconnect()
    
    async def get_one(self, id: str):
        return await self.database.get_one(id, self.schema)
    
    async def get_all(self, query: str):
        return await self.database.get_all(query, self.schema)
    
    async def create_one(self, data: dict):
        return await self.database.create_one(data, self.schema)
    
    async def update_one(self, id: str, data: dict):
        return await self.database.update_one(id, data, self.schema)
    
    async def delete_one(self, id: str):
        return await self.database.delete_one(id, self.schema)