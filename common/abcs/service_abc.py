from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import TypeVar, Generic

TCreate = TypeVar('TCreate', bound=BaseModel)
TUpdate = TypeVar('TUpdate', bound=BaseModel)
TGet = TypeVar('TGet', bound=BaseModel)
TQuery = TypeVar('TQuery', bound=BaseModel)
T = TypeVar('T', bound=BaseModel)

class ServiceABC(Generic[TCreate, TUpdate, TGet, TQuery, T], ABC):
    @abstractmethod
    async def create(self, data: TCreate) -> T:
        pass

    @abstractmethod
    async def update(self, id: str, data: TUpdate) -> T:
        pass

    @abstractmethod
    async def get_one(self, id: str) -> T:
        pass

    @abstractmethod
    async def get_all(self, query: TQuery) -> list[T]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass