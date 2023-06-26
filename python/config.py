import os
import secrets
import logging.config
from pathlib import Path
from typing import Optional
from fastapi import HTTPException, status
from fastapi.responses import Response
from pydantic import BaseSettings


class RequiresLoginException(Exception):
    pass


current_dir = os.path.dirname(__file__)


class Settings(BaseSettings):
    SECRET_KEY: str
    db_name: str
    db_username: Optional[str] = None    
    db_id = 0
    celery_url:Optional[str] = None
    bucket_name:Optional[str] = "lp_bucket"
    namespace_name:Optional[str] = "idqwmrl2shui"

    
    class Config:
        env_file = ".env"


settings = Settings()


class UserError(Exception):
    message: str

    def __init__(self, msg):
        self.message = msg


dir_name = os.path.split(current_dir)[1]
root_dir = os.path.abspath(os.path.dirname(current_dir))

# logging.config.fileConfig(
#     f"./{dir_name}/logging.ini", disable_existing_loggers=False)


userdata_path = os.path.join(os.path.abspath(
    os.path.dirname(current_dir)), 'userData')
    

# ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# SECRET_KEY: str = secrets.token_urlsafe(32)
SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM

user_not_authorized = Response(status_code=status.HTTP_403_FORBIDDEN,
                               headers={"WWW-Authenticate": "Bearer"},
                               content="User not Authorized to access this API")


def user_error(content_msg):
    return Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    headers={"WWW-Authenticate": "Bearer"},
                    content=content_msg)
