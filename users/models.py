from pydantic import BaseModel

class UserModel(BaseModel):
    id: str | None = None
    username: str | None = None
    email: str | None = None
    password: str | None = None
    shard_key: str | None = None

    class Config:
        orm_mode = True 

class UserModelCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True

class UserModelUpdate(BaseModel):
    id: str
    username: str | None = None
    email: str | None = None
    password: str | None = None
    shard_key: str | None = None

    class Config:
        orm_mode = True

class UserModelDelete(BaseModel):
    id: int

    class Config:
        orm_mode = True