from database_service.hash_factory import HashFactorySingleton
from database_service.mysql_service import MySQLServiceSingleton
from common.abcs.startup_tasks_abc import StartupTasksABC
from common import get_databases
from database_service.redis_service import RedisServiceSingleton
import os

class StartupTasks(StartupTasksABC):
    @staticmethod
    async def add_database_to_hash_ring():
        databases = get_databases()

        hash_factory = HashFactorySingleton()
        for database in databases:
            await database.connect()
            hash_factory.add_database(database)
    

    @staticmethod
    async def load():
        await StartupTasks.add_database_to_hash_ring()
        await RedisServiceSingleton().connect()
        print("Startup tasks completed successfully.")

