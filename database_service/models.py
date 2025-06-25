from pydantic import BaseModel

class QueryModel(BaseModel):
    skip: int = 1
    limit: int = 10
    sort_by: str = "created_at"
    sort_order: str = "asc"
    filter: dict = {}
    fields: list[str] = []