from database_service.abc_classes import DatabaseABC
from database_service.mysql_service import MySQLServiceSingleton

class HashFactory:
    def __init__(self, hash_algorithm = None, databases = None, hash_rings = None):
        self.hash_algorithm = hash_algorithm
        self.databases = databases or []
        self.hash_rings = hash_rings or {}
    
    def get_db_by_key(self, key: str) -> 'DatabaseABC':
        return MySQLServiceSingleton()  # For simplicity, returning MySQLServiceSingleton directly.
        # In a real implementation, we need to use the hash_algorithm to determine which database to return.
