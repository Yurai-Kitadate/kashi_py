from sqlalchemy import Column, Integer, String
from api.db import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50))