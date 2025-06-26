from abc import ABC, abstractmethod
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from typing import Generic, TypeVar

S = TypeVar('S', bound=DeclarativeBase)
T = TypeVar('T', bound=BaseModel)

class DatabaseABC(Generic[S, T], ABC):
    @abstractmethod
    def get_db_url(self) -> str:
        """return db url"""
        pass

    @abstractmethod
    async def connect(self):
        """Establish a connection to the database."""
        pass

    @abstractmethod
    async def disconnect(self):
        """Close the connection to the database."""
        pass

    @abstractmethod
    async def create_metadata(self, schema: S):
        pass

    @abstractmethod
    async def create_one(self, data: T, schema: S) -> S:
        """Create a single record in the database."""
        pass

    @abstractmethod
    async def get_one(self, id: str, schema: S) -> S:
        """Read a single record from the database by its ID."""
        pass

    @abstractmethod
    async def get_all(self, query: T, schema: S) -> list[S]:
        """Read all records from the database."""
        pass

    @abstractmethod
    async def update_one(self, id: str, data: T, schema: S) -> S:
        """Update a single record in the database."""
        pass

    @abstractmethod
    async def delete_one(self, id: str, schema: S) -> None:
        """Delete a single record from the database."""
        pass