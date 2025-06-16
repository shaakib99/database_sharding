from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run at startup
    yield
    # Code to run at shutdown

app = FastAPI(lifespan=lifespan)