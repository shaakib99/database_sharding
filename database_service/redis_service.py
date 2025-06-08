from redis import Redis

class RedisService:
    def __init__(self):
        self.redis_client = Redis(host='localhost', port=6379, db=0)
    
    async def connect(self):
        self.redis_client.ping()

    async def disconnect(self):
        self.redis_client.close()

    async def set_value(self, key, value):
        await self.redis_client.set(key, value)

    async def get_value(self, key):
        return await self.redis_client.get(key)

    async def delete_value(self, key):
        await self.redis_client.delete(key)

    async def exists(self, key):
        return self.redis_client.exists(key)

class RedisServiceSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = RedisService()
        return cls._instance