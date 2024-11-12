from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from database import engine

class UserRole(Base):
    __tablename__ = "user_role" 

    type_id = Column(Integer, primary_key=True)
    usertype = Column(String(50))

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    roleid = Column(Integer, ForeignKey("user_role.type_id")) 

Base.metadata.create_all(bind=engine)