from fastapi import APIRouter
from .service import UsersService
from database_service.models import QueryModel
from .models import CreateUserModel, UpdateUserModel, UserModel
from typing import Annotated

users_router = APIRouter(prefix='/user')

users_service = UsersService()

@users_router.get('/{id}')
async def get_one(id: str):
    return await users_service.get_one(id)

@users_router.get('')
async def get_all(query: Annotated[QueryModel, dict]):
    return await users_service.get_all(query)

@users_router.post('')
async def create_one(data: CreateUserModel):
    return await users_service.create_one(data)

@users_router.put('/{id}')
async def update_one(id: str, data: UpdateUserModel):
    return await users_service.update_one(id, data)

@users_router.delete('/{id}')
async def delete_one(id: str):
    return await users_service.delete_one(id)