from typing_extensions import Self
from redis import Redis
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar(name='T', bound=BaseModel)

class RedisService(Generic[T]):
    def __init__(self, host: str, port: int):
        self.redis_client = Redis(host=host, port=port)
    
    async def get(self, key: str) -> T | None:
        data = await self.redis_client.get(key)
        if not data: return data.model_validate()
        return None
    
    async def put(self, key: str, data: T):
        self.redis_client.set(key, data.model_dump().__str__())

class RedisServiceSingleTon:
    _instance = None

    def __new__(cls, host: str, port: int) -> "RedisService":
        if cls._instance is None:
            cls._instance = RedisService(host, port)
        return cls._instance