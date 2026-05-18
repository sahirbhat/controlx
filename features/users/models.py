from sqlalchemy import Column, Integer, String, Boolean
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="developer")
    is_active = Column(Boolean, default=True)
    phone = Column(String(15), nullable=True)