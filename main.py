from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from startup_tasks import StartupTasks

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

@app.get("/")
async def root():
    return {"message": "Hello World"}
