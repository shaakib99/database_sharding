from database_service.abc_classes import DatabaseABC
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from common.exceptions import NotFoundException
from functools import cache
from users import UsersBase
from typing import Type, TypeVar
from pydantic import BaseModel


class MySQLService(DatabaseABC):
    def __init__(self, url: str):
        self.engine = create_engine(url, echo=True, future=True, pool_pre_ping=True, pool_size=5, max_overflow=10)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.create_metadata()

    async def connect(self):
        self.engine.connect()

    async def disconnect(self):
        self.engine.dispose()
    
    def create_metadata(self):
        tables: list[DeclarativeBase] = [UsersBase]
        for table in tables:
            table.metadata.create_all(bind=self.engine)


    async def get_one(self, id, schema: Type[DeclarativeBase]):
        cursor = self.session.query(schema)
        result = cursor.filter_by(id=id).first()
        if result is None:
            raise NotFoundException("Not Found")
        return result

    async def get_all(self, query, schema: Type[DeclarativeBase]):
        cursor = self.session.query(schema)
        cursor = cursor.limit(query.limit)
        cursor = cursor.offset(query.skip)
        if query.sort:
            cursor = cursor.order_by(query.sort)
        if query.filter:
            for key, value in query.filter.items():
                cursor = cursor.filter(getattr(schema, key) == value)
        if query.fields:
            cursor = cursor.with_entities(*[getattr(schema, field) for field in query.fields])

        return cursor.all()


    async def create_one(self, data: BaseModel, schema: Type[DeclarativeBase]):
        new_record = schema(**data.model_dump())
        self.session.add(new_record)
        self.session.commit()
        return new_record

    async def update_one(self, id, data:BaseModel, schema: Type[DeclarativeBase]):
        record = await self.get_one(id, schema)
        for key, value in data.model_dump().items():
            setattr(record, key, value)
        self.session.commit()
        return record

    async def delete_one(self, id: str, schema: Type[DeclarativeBase]):
        record = await self.get_one(id, schema)
        self.session.delete(record)
        self.session.commit()
        return None

class MySQLServiceSingleton:
    _instance_mapper = {}
    def __new__(cls, url: str) -> 'MySQLService':
        if url not in cls._instance_mapper:
            cls._instance_mapper[url] = MySQLService(url)
        return cls._instance_mapper[url]