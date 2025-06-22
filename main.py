from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from users_service.route import users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run at startup
    load_dotenv()
    yield
    # Code to run at shutdown

app = FastAPI(lifespan=lifespan)

routers: list[APIRouter] = [users_router]
for router in routers:
    app.include_router(router)