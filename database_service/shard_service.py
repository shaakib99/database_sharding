from database_service.redis_service import RedisService, RedisServiceSingleton
from database_service.hash_factory import HashFactorySingleton, HashFactory
from database_service.abc_classes import DatabaseABC
class ShardService:
    def __init__(self, redis_service: RedisService | None, hash_service: HashFactory | None) -> None:
        self.redis_service = redis_service or RedisServiceSingleton()
        self.hash_service = hash_service or HashFactorySingleton()
    
    async def get_shard_key_from_id(self, id: str) -> str:
        shard_key = id
        while await self.redis_service.get_value(shard_key) != shard_key:
            shard_key = await self.redis_service.get_value(shard_key)
            if shard_key is None:
                raise ValueError(f"Shard key not found for id: {id}")
        return shard_key

    async def get_database_from_id(self, id: str) -> 'DatabaseABC':
        shard_key = await self.get_shard_key_from_id(id)
        return self.hash_service.get_database_by_key(shard_key)
    
    async def add_id_to_shard(self, id: str, shard_key: str) -> None:
        if not await self.redis_service.exists(shard_key):
            raise ValueError(f"Shard key {shard_key} does not exist in Redis")
        await self.redis_service.set_value(id, shard_key)

class ShardServiceSingleton:
    _instance = None

    def __new__(cls, redis_service: RedisService | None = None, hash_service: HashFactory | None = None) -> 'ShardService':
        if cls._instance is None:
            cls._instance = ShardService(redis_service, hash_service)
        return cls._instance