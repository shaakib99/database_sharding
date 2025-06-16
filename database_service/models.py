from pydantic import BaseModel

class QueryModel(BaseModel):
    """Base model for query parameters."""
    page: int = 1
    limit: int = 10
    sort_by: str = "created_at"
    sort_order: str = "asc"