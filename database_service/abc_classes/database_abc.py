from abc import ABC, abstractmethod
from sqlalchemy.orm import DeclarativeBase 
from pydantic import BaseModel
from common import CommonQueryModel
from typing import Type, Generic, TypeVar

T = TypeVar('T', bound=DeclarativeBase)

class DatabaseABC(Generic[T], ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def get_one(self, id: str, schema: Type[DeclarativeBase]) -> T:
        pass

    @abstractmethod
    async def get_all(self, query: CommonQueryModel, schema: Type[DeclarativeBase]) -> list[T]:
        pass

    @abstractmethod
    async def create_one(self, data: BaseModel, schema: Type[DeclarativeBase]) -> T:
        pass

    @abstractmethod
    async def update_one(self, id: str, data: BaseModel, schema: Type[DeclarativeBase]) -> T:
        pass

    @abstractmethod
    async def delete_one(self, id: str, schema: Type[DeclarativeBase]) -> None:
        pass

