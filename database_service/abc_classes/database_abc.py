from abc import ABC, abstractmethod
from typing import Any

class DatabaseABC(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass
    
    @abstractmethod
    async def get_one(self, id: str, schema):
        pass

    @abstractmethod
    async def get_all(self, query, schema):
        pass

    @abstractmethod
    async def create_one(self, data, schema):
        pass

    @abstractmethod
    async def update_one(self, id: str, data, schema):
        pass

    @abstractmethod
    async def delete_one(self, id: str, schema):
        pass

