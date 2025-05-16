from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    load_dotenv()
    yield
    # Code to run on shutdown


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}
