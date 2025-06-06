from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from startup_tasks import StartupTasks
from users import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    load_dotenv()
    # Load startup tasks
    _ = StartupTasks()
    await StartupTasks.load()
    yield
    # Code to run on shutdown


app = FastAPI(lifespan=lifespan)

routers: list[APIRouter] = [user_router]
for router in routers:
    app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
