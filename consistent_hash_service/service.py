from database_service.redis_service.service import RedisService
from database_service.abcs.database_abc import DatabaseABC
import hashlib

class ConsistentHashService:
    def __init__(self, number_of_slots = 1000, redis_service: RedisService | None = None):
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
            
    async def add_database_in_hash_ring(self, id: str, database: DatabaseABC):
        pass

    async def remove_database_from_hash_ring(self, database: DatabaseABC):
        pass