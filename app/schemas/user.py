from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    username:str = Field(...,min_length=3,max_length=50,description="用户名")
    email:EmailStr
    password: str = Field(..., min_length=6, max_length=128, description="密码")

class UserOut(BaseModel):
    id:int
    email:EmailStr
    username:str
    is_active:bool
    created_at:datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str = "bearer"
