from database_service.redis_service.service import RedisService
from database_service.abcs.database_abc import DatabaseABC
from database_service.models import QueryModel
from common.utils import get_all_schemas_in_order
import hashlib

class ConsistentHashService:
    def __init__(self, number_of_slots = 1000, redis_service: RedisService | None = None, database_service: DatabaseABC | None = None):
        self.hash_ring: list[DatabaseABC | None] = [None] * number_of_slots
        self.number_of_slots = number_of_slots
        self.redis_service = redis_service or RedisService('localhost', 6379)

    def _hash(self, s: str) -> int:
        return int(hashlib.md5(s.encode()).hexdigest(), 16)
    
    async def get_database_from_unique_id(self, id: str) -> DatabaseABC:
        database_index = self._hash(id) % self.number_of_slots
        original_database_index =  database_index
        while self.hash_ring[database_index] is None and database_index < len(self.hash_ring):
            database_index += 1
        
        if database_index == len(self.hash_ring):
            database_index = 0

        while self.hash_ring[database_index] is None and database_index < original_database_index:
            database_index += 1
        
        database = self.hash_ring[database_index]

        if database is  None: raise ValueError(f'Database not found for id {id}') 
        return database
    
    def _find_next_database_from_index(self, index: int):
        source_database_index = index + 1
        while source_database_index < len(self.hash_ring) and self.hash_ring[source_database_index] is None:
            source_database_index += 1
        
        if source_database_index == len(self.hash_ring):
            source_database_index = 0
        
        while source_database_index < index and self.hash_ring[source_database_index] is None:
            source_database_index += 1

        return self.hash_ring[source_database_index]
            
    async def add_database_in_hash_ring(self, database: DatabaseABC):
        index = self._hash(database.__str__()) % self.number_of_slots
        if self.hash_ring[index] is not None: raise ValueError('Database already exist')
        
        source_database = self._find_next_database_from_index(index)
        delete_keys = []
        if source_database is not None:
            for schema in get_all_schemas_in_order(): 
                delete_keys = await self.redistribute_keys(source_database, database, schema)

        self.hash_ring[index] = database

        await self.remove_keys(source_database, delete_keys)

    async def remove_database_from_hash_ring(self, database: DatabaseABC):
        index = self._hash(database.__str__()) % self.number_of_slots
        if self.hash_ring[index] is None: raise ValueError('Database does not exist')
        
        target_database = self._find_next_database_from_index(index)
        if target_database is None: raise ValueError('Can not move keys. No other database exist')

        delete_keys = []
        for schema in get_all_schemas_in_order():
            delete_keys = await self.redistribute_keys(database, target_database, schema)
            
        self.hash_ring[index] = None

        await self.remove_keys(database, delete_keys)
    
    async def redistribute_keys(self, source_database: DatabaseABC, target_database: DatabaseABC, schema):
        await source_database.create_metadata(schema)
        await target_database.create_metadata(schema)

        query_model = QueryModel()
        source_data = await source_database.get_all(query_model, schema)
        delete_data = []
        for item in source_data:
            if self.get_database_from_unique_id(item.id) != target_database: continue
            await target_database.create_one(item, schema)
            delete_data.append((item, schema))
        return delete_data

    
    async def remove_keys(self, database, keys: list):
        for item, schema in keys:
            await database.delete_one(item.id, schema)
    
    async def get_all_database(self):
        databases: list[DatabaseABC] = []
        for database in self.hash_ring:
            if database is not None: databases.append(database)
        return databases
    
    async def get_database_from_key(self, id: str):
        temp_id = (await self.redis_service.get(id))
        while temp_id is not None:
            temp_id = await self.redis_service.get(id)
            if temp_id is None: break
            id = temp_id
        return await self.get_database_from_unique_id(id)

    async def join_ids(self, id: str, shard_id):
        await self.redis_service.put(id, shard_id)

class ConsistentHashServiceSingleton:
    _instance = None
    def __new__(cls) -> 'ConsistentHashService':
        if cls._instance is None:
            cls._instance = ConsistentHashService()
        return cls._instance