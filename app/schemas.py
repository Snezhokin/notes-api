from pydantic import BaseModel , EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str 
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id:int
    username:str
    email:EmailStr
    created_at:datetime
    
    class Config:
        from_attributes=True

class NoteCreate(BaseModel):
    title:str
    content: Optional[str] = None

class NoteOut(BaseModel):
    id:int
    title:str
    content:Optional[str]=None
    created_at:datetime
    updated_at:datetime
    user_id:int

    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token:str
    token_type:str