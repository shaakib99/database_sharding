from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from users_service.route import users_router
from common.utils import get_all_schemas_in_order
from database_service.service import DatabaseService
from consistent_hash_service.service import ConsistentHashServiceSingleton
from database_service.mysql_service.service import MySQLServiceSingleton
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run at startup
    load_dotenv()
    

    # Add database in hash ring
    consistent_hash_service = ConsistentHashServiceSingleton()
    await consistent_hash_service.init_hash_ring()
    database_urls: list[str] = os.getenv('AVAILABLE_DATABASES', '').split(',') 
    databases = []
    for url in database_urls:
        if not url: continue
        database = MySQLServiceSingleton(url)
        await database.connect()
        await consistent_hash_service.add_database_in_hash_ring(database)
        databases.append(database)

    # create metadata
    schemas = get_all_schemas_in_order()
    for schema in schemas:
        await DatabaseService(schema).create_metadata()

    yield
    # Code to run at shutdown
    # disconnect from database
    for database in databases:
        await database.disconnect()

app = FastAPI(lifespan=lifespan)

routers: list[APIRouter] = [users_router]
for router in routers:
    app.include_router(router)