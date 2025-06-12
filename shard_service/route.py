from fastapi import APIRouter
from database_service.mysql_service import MySQLServiceSingleton
from shard_service import CreateShardModel, ShardService
from database_service.hash_factory import HashFactorySingleton

shard_service_router = APIRouter(prefix="/shard")

hash_factory = HashFactorySingleton()

@shard_service_router.post("/add")
async def add_shard(data: CreateShardModel):
    url: str = data.url
    database = MySQLServiceSingleton(url=url)
    hash_factory.add_database(database)

    return {"message": f"Shard added successfully."}