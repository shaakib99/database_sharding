from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String
 
UsersBase =  declarative_base()

class UserSchema(UsersBase):
    __tablename__ = 'users'
    
    id = Column(String(62), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    shard_key = Column(String(60), nullable=False)