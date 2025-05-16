from fastapi import APIRouter

monitoring_router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@monitoring_router.post("/db/add")
async def add_db_entry(entry: dict):
    pass

@monitoring_router.get("/db/remove")
async def remove_db_entry(entry_id: str):
    pass