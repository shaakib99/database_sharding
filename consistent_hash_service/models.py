from pydantic import BaseModel

class CreateDatabaseModel(BaseModel):
    url: str