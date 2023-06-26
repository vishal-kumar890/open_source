from pydantic import BaseModel, EmailStr
from typing import Optional, Any


class Token(BaseModel):
    access_token: str
    token_type: str


class signupUser(BaseModel):
    full_name: str
    password: str
    email: str


class resetPassword(BaseModel):
    old_password: str
    new_password: str


class User(BaseModel):
    email: Optional[str] = None
    contact: Optional[str] = None
    id: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    profile_pic: Optional[str] = None
