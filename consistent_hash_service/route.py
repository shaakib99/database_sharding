from fastapi import APIRouter
from .service import ConsistentHashServiceSingleton
from .models import CreateDatabaseModel
from database_service.mysql_service.service import MySQLServiceSingleton

hash_ring_router = APIRouter(prefix='/hash_ring')
hash_ring_service = ConsistentHashServiceSingleton()

@hash_ring_router.post('/add')
async def add_database_in_hash_ring(data: CreateDatabaseModel):
    database = MySQLServiceSingleton(data.url)
    return await hash_ring_service.add_database_in_hash_ring(database)

@hash_ring_router.post('/remove')
async def remove_database_in_hash_ring(data: CreateDatabaseModel):
    database = MySQLServiceSingleton(data.url)
    return await hash_ring_service.remove_database_from_hash_ring(database)