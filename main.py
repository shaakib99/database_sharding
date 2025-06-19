from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run at startup
    load_dotenv()
    yield
    # Code to run at shutdown

app = FastAPI(lifespan=lifespan)