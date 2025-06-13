
from database_service.hash_factory import HashFactory
from database_service import DatabaseABC
from database_service.mysql_service import MySQLServiceSingleton
from database_service.service import DatabaseService
from common.models.common_query_model import CommonQueryModel
from shard_service.shard_service import ShardService, ShardServiceSingleton
from pydantic import BaseModel

class KeyRedistributionService:
    def __init__(self, schema, shard_service: ShardService, database_service: DatabaseABC, model: BaseModel):
        self.schema = schema
        self.shard_service = shard_service or ShardServiceSingleton()
        self.database_service = database_service
        self.model = model

    async def redistribute_keys(self, target_database_url: str, source_database_url: str):
        target_database = MySQLServiceSingleton(target_database_url)
        source_database = MySQLServiceSingleton(source_database_url)

        data = await source_database.get_all(CommonQueryModel(), self.schema)
        
        for item in data:
            _datamodel = self.model.model_validate(item)
            id_value = getattr(_datamodel, "id", None)
            if id_value is None: continue
            target_db = await self.shard_service.get_database_from_id(id_value)

            if target_db == target_database:
                await target_database.create_one(_datamodel, self.schema)
                await source_database.delete_one(id_value, self.schema)