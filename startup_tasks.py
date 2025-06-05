from database_service.hash_factory import HashFactorySingleton
from database_service.mysql_service import MySQLServiceSingleton
from common.abcs.startup_tasks_abc import StartupTasksABC
import os

class StartupTasks(StartupTasksABC):
    @staticmethod
    async def add_database_to_hash_ring():
        database_urls = os.getenv('AVAILABLE_DATABASES', '').split(',')

        hash_factory = HashFactorySingleton()
        for database_url in database_urls:
            database = MySQLServiceSingleton(database_url.strip())
            await database.connect()
            hash_factory.add_database(database)
    

    @staticmethod
    async def load():
        await StartupTasks.add_database_to_hash_ring()
        print("Startup tasks completed successfully.")