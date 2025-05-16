from pydantic import BaseModel
from typing import Optional

class CommonQueryModel(BaseModel):
    limit: int = 10
    skip: int = 0
    sort: Optional[str] = None
    filter: dict = {}
    fields: list = []