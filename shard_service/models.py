from pydantic import BaseModel

class CreateShardModel(BaseModel):
    url: str