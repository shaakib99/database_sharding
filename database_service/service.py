from database_service.abcs.database_abc import DatabaseABC
from .abcs.database_service_abc import DatabaseServiceABC
from .mysql_service.service import MySQLServiceSingleton

class DatabaseService(DatabaseServiceABC):
    def __init__(self, schema):
        self.schema = schema
    
    async def create_one(self, data):
        database = MySQLServiceSingleton('test')
        return await database.create_one(data, self.schema)
    
    async def update_one(self, id: str, data):
        database = MySQLServiceSingleton('test')
        return await database.update_one(id, data, self.schema)
    
    async def get_one(self, id: str):
        database = MySQLServiceSingleton('test')
        return database.get_one(id, self.schema)
    
    async def get_all(self, query) -> list:
        database = MySQLServiceSingleton('test')
        return await database.get_all(query, self.schema)
    
    async def create_using_selected_database(self, data, database):
        return await database.create_one(data, self.schema)
    
    async def update_using_selected_database(self, id: str, data, database):
        return await database.update_one(id, data, self.schema)
    
    async def delete_using_selected_database(self, id: str, database: DatabaseABC):
        return await database.delete_one(id, self.schema)