from typing_extensions import Self
from database_service.abc_classes import DatabaseABC
import bisect

class HashFactory:
    def __init__(self, number_of_slots = 10000):
        self.hash_rings: list[DatabaseABC | None] = [None for _ in range(number_of_slots)]
        self.number_of_slots = number_of_slots
    
    def get_database_by_key(self, key: str) -> 'DatabaseABC':
        index = hash(key) % self.number_of_slots
        database = self.hash_rings[index]
        if database is not None:
            return database
        for i in range(self.number_of_slots):
            next_index = (index + i) % self.number_of_slots
            database = self.hash_rings[next_index]
            if database is not None:
                return database
        raise ValueError('No database found for the given key')
        
    def add_database(self, database: DatabaseABC):
        database_index = hash(database) % self.number_of_slots
        if self.hash_rings[database_index] is None:
            self.hash_rings[database_index] = database

        raise ValueError('Database already exists in the hash ring')

    def remove_database(self, database: DatabaseABC):
        database_index = hash(database) % self.number_of_slots
        if self.hash_rings[database_index] == database:
            self.hash_rings[database_index] = None

        raise ValueError('Database not found in the hash ring')

class HashFactorySingleton:
    _instance = None

    def __new__(cls) -> 'HashFactory':
        if cls._instance is None:
            cls._instance = HashFactory()
        return cls._instance