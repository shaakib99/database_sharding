from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
 
UsersBase =  declarative_base()

class UserSchema(UsersBase):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    shard_key = Column(String(600), nullable=False)