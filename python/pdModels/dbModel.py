from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from enum import Enum



class user_db(BaseModel):
    db_type: Optional[str] = "SQLITE"
    db_id: int
    db_host: Optional[str] = None
    db_name: Optional[str] = None
    db_port: Optional[int] = None
    db_username: Optional[str] = None
    db_password: Optional[str] = None

    @validator('db_host')
    def host_required_if_not_sqlite(cls, v, values, **kwargs):
        return v

    @validator('db_port')
    def port_required_if_not_sqlite(cls, v, values, **kwargs):
        return v

    @validator('db_username')
    def username_required_if_not_sqlite(cls, v, values, **kwargs):
        return v

    @validator('db_password')
    def password_required_if_not_sqlite(cls, v, values, **kwargs):
        return v
