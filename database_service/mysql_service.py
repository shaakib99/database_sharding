from database_service.abc_classes import DatabaseABC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from common.exceptions import NotFoundException

class MySQLService(DatabaseABC):
    def __init__(self):
        self.engine = create_engine('mysql+aiomysql://user:password@localhost/dbname')
        self.Session = sessionmaker(bind=self.engine, class_=AsyncSession)
        self.session = self.Session()
    
    async def connect(self):
        self.engine.connect()

    async def disconnect(self):
        self.engine.dispose()

    async def get_one(self, id, schema):
        cursor = self.session.query(schema)
        result = cursor.filter_by(id=id).first()
        if result is None:
            raise NotFoundException("Not Found")
        return result

    async def get_all(self, query, schema):
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


    async def create_one(self, data, schema):
        new_record = schema(**data.dict())
        self.session.add(new_record)
        self.session.commit()
        return new_record

    async def update_one(self, id, data, schema):
        record = await self.get_one(id, schema)
        for key, value in data.model_dump().items():
            setattr(record, key, value)
        self.session.commit()
        return record

    async def delete_one(self, id, schema):
        record = await self.get_one(id, schema)
        self.session.delete(record)
        self.session.commit()
        return None

class MySQLServiceSingleton:
    _instance = None

    def __new__(cls) -> 'MySQLService':
        if cls._instance is None:
            cls._instance = MySQLService()
        return cls._instance