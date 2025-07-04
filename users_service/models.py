from pydantic import BaseModel

class UserModel(BaseModel):
    id: str | None = None
    username: str | None = None
    password: str | None = None
    email: str | None = None
    shard_id: str | None = None

    class Config:
        from_attributes = True

class CreateUserModel(BaseModel):
    username: str
    password: str
    email: str

class UpdateUserModel(BaseModel):
    username: str | None = None
    password: str | None = None