from sqlalchemy import String, Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__="users"

    id =Column(Integer , primary_key=True , index=True)
    username =Column(String, unique=True, index=True ,nullable=False)
    email=Column(String , unique=True, index= True, nullable=False)
    hashed_password=Column(String, nullable=False)
    created_at=Column(DateTime , default=datetime.utcnow)

    notes= relationship("Note", back_populates="owner",cascade="all, delete_orphan")

class Note(Base):
    __tablename__="notes"

    id=Column(Integer, primary_key=True,index=True)
    title=Column(String,index=True,nullable=False)
    content=Column(Text, nullable=False)
    created_at=Column(DateTime , default=datetime.utcnow)
    updated_at=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id= Column(Integer, ForeignKey("users.id"),nullable=False )

    owner =relationship("User", back_poopulates ="notes")



