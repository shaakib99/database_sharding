from abc import ABC, abstractmethod
from sqlalchemy.orm import DeclarativeBase
from typing import TypeVar, Type, Generic
from pydantic import BaseModel
from database_service.abcs.database_abc import DatabaseABC

S = TypeVar('S', bound=DeclarativeBase)
T = TypeVar('T', bound=BaseModel)

class DatabaseServiceABC(Generic[S, T], ABC):
    def __init__(self, schema: Type[S]):
        pass

    @abstractmethod
    async def connect(self) -> None:
        """Establish a connection to the database."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close the connection to the database."""
        pass

    @abstractmethod
    async def create_one(self, data: T) -> S:
        """Create a single record in the database."""
        pass

    @abstractmethod
    async def get_one(self, id: str) -> S:
        """Read a single record from the database by its ID."""
        pass

    @abstractmethod
    async def get_all(self, query: T) -> list[S]:
        """Read all records from the database."""
        pass

    @abstractmethod
    async def update_one(self, id: str, data: T) -> S:
        """Update a single record in the database."""
        pass

    @abstractmethod
    async def delete_one(self, id: str) -> None:
        """Delete a single record from the database."""
        pass

    @abstractmethod
    async def create_using_selected_database(self, data: T, database: DatabaseABC) -> S:
        """Create a single record in the selected database."""
        pass

    @abstractmethod
    async def update_using_selected_database(self, id: str, data: T, database: DatabaseABC):
        """Update a single record in the selected database"""
    
    @abstractmethod
    async def delete_using_selected_database(self, id: str, database: DatabaseABC):
        """Delete a single in the selected database"""
    