from fastapi.routing import APIRouter
from . import UserModel, UserModelCreate, UserModelUpdate, UsersService
from common import CommonQueryModel


user_router = APIRouter(prefix="/users")

users_service = UsersService()

@user_router.get("/", response_model=UserModel)
async def get_users(query: CommonQueryModel):
    return await users_service.get_all(query)

@user_router.get("/{id}", response_model=UserModel)
async def get_user(id: str):
    return await users_service.get_one(id)

@user_router.post("/", response_model=UserModel)
async def create_user(user: UserModelCreate):
    return await users_service.create(user)

@user_router.put("/{id}", response_model=UserModel)
async def update_user(id: str, user: UserModelUpdate):
    return await users_service.update(id, user)

@user_router.delete("/{id}", response_model=None)
async def delete_user(id: str):
    return await users_service.delete(id)