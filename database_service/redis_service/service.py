from redis import Redis
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar(name='T', bound=BaseModel)

class RedisService(Generic[T]):
    def __init__(self, host: str, port: int):
        self.redis_client = Redis(host=host, port=port, decode_responses=True)
    
    async def connect(self):
        self.redis_client.ping()
    
    async def disconnect(self):
        self.redis_client.quit()
    
    async def get(self, key: str):
        data = self.redis_client.get(key)
        return data
    
    async def put(self, key: str, data: str):
        self.redis_client.set(key, data)

class RedisServiceSingleTon:
    _instance = None

    def __new__(cls, host: str, port: int) -> "RedisService":
        if cls._instance is None:
            cls._instance = RedisService(host, port)
        return cls._instance