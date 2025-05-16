from abc import ABC, abstractmethod
from sqlalchemy.ext.declarative import DeclarativeMeta 
from pydantic import BaseModel
from common import CommonQueryModel

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
    async def get_one(self, id: str, schema: DeclarativeMeta) -> DeclarativeMeta:
        pass

    @abstractmethod
    async def get_all(self, query: CommonQueryModel, schema: DeclarativeMeta) -> list[DeclarativeMeta]:
        pass

    @abstractmethod
    async def create_one(self, data: BaseModel, schema: DeclarativeMeta) -> DeclarativeMeta:
        pass

    @abstractmethod
    async def update_one(self, id: str, data: BaseModel, schema: DeclarativeMeta) -> DeclarativeMeta:
        pass

    @abstractmethod
    async def delete_one(self, id: str, schema: DeclarativeMeta) -> None:
        pass

