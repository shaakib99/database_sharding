from database_service.abc_classes import DatabaseABC
from database_service.redis_service import RedisService
import hashlib

class HashFactory:
    def __init__(self, number_of_slots = 10000):
        self.hash_rings: list[DatabaseABC | None] = [None for _ in range(number_of_slots)]
        self.number_of_slots = number_of_slots
    
    def _hash(self, key:str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def get_database_by_key(self, key: str) -> 'DatabaseABC':
        index = self._hash(key) % self.number_of_slots
        visited_index = set()

        while self.hash_rings[index] is None and index < self.number_of_slots:
            visited_index.add(index)
            index += 1


        if index >= self.number_of_slots:
            index = 0
            while self.hash_rings[index] is None and index not in visited_index:
                visited_index.add(index)
                index += 1
            
        database = self.hash_rings[index]
        if database is not None:
            return database
        
        raise ValueError('No database found for the given key')
        
    def add_database(self, database: DatabaseABC):
        database_index = self._hash(str(database)) % self.number_of_slots
        print(f"Adding database at index {database_index} with hash {self._hash(str(database))}, {self.hash_rings[database_index]}")
        if self.hash_rings[database_index] is None:
            self.hash_rings[database_index] = database
            return

        raise ValueError('Database already exists in the hash ring')

    def remove_database(self, database: DatabaseABC):
        database_index = self._hash(str(database)) % self.number_of_slots
        while self.hash_rings[database_index] is None and database_index < self.number_of_slots:
            database_index += 1

        if database_index >= self.number_of_slots:
            raise ValueError('Database not found in the hash ring')
        

        if database == self.hash_rings[database_index]:
            self.hash_rings[database_index] = None
            return

        raise ValueError('Database not found in the hash ring')

class HashFactorySingleton:
    _instance = None

    def __new__(cls) -> 'HashFactory':
        if cls._instance is None:
            cls._instance = HashFactory()
        return cls._instance