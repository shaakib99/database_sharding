from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer

UserBase = declarative_base()

class UserSchema(UserBase):
    __tablename__ = 'users'

    id = Column(String(65), autoincrement=False, nullable=False, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    shard_id = Column(String(15), nullable=False)