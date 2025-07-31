from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)