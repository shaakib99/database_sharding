from ..abcs.database_abc import DatabaseABC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.exceptions import NotFoundException

class MySQLService(DatabaseABC):
    def __init__(self, url: str):
        self.url = url
        self.engine = create_engine(url)
        self.session = sessionmaker(bind=self.engine)()
    
    async def connect(self):
        """Establish a connection to the MySQL database."""
        self.engine.connect()

    async def disconnect(self):
        """Close the connection to the MySQL database."""
        self.engine.dispose()
    
    async def create_metadata(self, schema):
        schema.metadata.create_all(bind=self.engine)

    async def create_one(self, data, schema):
        """Create a single record in the MySQL database."""
        data = schema(*data.model_dump())
        self.session.add(data)
        self.session.commit()
        self.session.flush()

    async def get_one(self, id: str, schema):
        """Read a single record from the MySQL database by its ID."""
        data = self.session.query(schema).first()
        if not data: raise NotFoundException('record not found')
        return data

    async def get_all(self, query, schema):
        """Read all records from the MySQL database."""
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

    async def update_one(self, id: str, data, schema):
        """Update a single record in the MySQL database."""
        record = self.get_one(id, schema)
        for key, value in data.model_dump().items():
            setattr(record, key, value)
        self.session.commit()
        return record

    async def delete_one(self, id: str, schema):
        """Delete a single record from the MySQL database."""
        record = self.get_one(id, schema)
        self.session.delete(record)
        self.session.commit()

class MySQLServiceSingleton:
    _instance = {}

    def __new__(cls, url: str) -> "DatabaseABC":
        if url in cls._instance: return cls._instance[url]
        cls._instance[url] = MySQLService(url)
        return cls._instance[url]
        