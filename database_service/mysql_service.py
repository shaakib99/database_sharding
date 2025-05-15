from typing import Any
from database_service.abc_classes import DatabaseABC

class MySQLService(DatabaseABC):
    instance = None
    def __init__(self):
        pass
    
    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def get_one(self, id: str, schema):
        pass

    async def get_all(self, query, schema):
        pass

    async def create_one(self, data, schema):
        pass

    async def update_one(self, id: str, data, schema):
        pass

    async def delete_one(self, id: str, schema):
        pass

class MySQLSingleton:
    _instance = None

    def __new__(cls) -> 'MySQLService':
        if cls._instance is None:
            cls._instance = MySQLService()
        return cls._instance