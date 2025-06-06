from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import TypeVar, Generic
from sqlalchemy.orm import DeclarativeBase

TCreate = TypeVar('TCreate', bound=BaseModel)
TUpdate = TypeVar('TUpdate', bound=BaseModel)
TGet = TypeVar('TGet', bound=BaseModel)
TQuery = TypeVar('TQuery', bound=BaseModel)
T = TypeVar('T', bound=BaseModel)
R = TypeVar('R', bound=DeclarativeBase)

class ServiceABC(Generic[TCreate, TUpdate, TGet, TQuery, T, R], ABC):
    @abstractmethod
    async def create(self, data: TCreate) -> R:
        pass

    @abstractmethod
    async def update(self, id: str, data: TUpdate) -> R:
        pass

    @abstractmethod
    async def get_one(self, id: str) -> R:
        pass

    @abstractmethod
    async def get_all(self, query: TQuery) -> list[R]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass