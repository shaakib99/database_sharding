from pydantic import BaseModel

class UserModel(BaseModel):
    id: str | None = None
    username: str | None = None
    password: str | None = None
    email: str | None = None

    class Config:
        orm_mode = True

class CreateUserModel(BaseModel):
    username: str
    password: str
    email: str