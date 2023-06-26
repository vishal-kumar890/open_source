from fastapi import Request, Depends, APIRouter
from ..core.sqlConnector import sqlConnect
from ..core import solveMethods as sm

router = APIRouter()

@router.post('/solve')
async def solve(data_dict:dict,request:Request):
    with sqlConnect() as conn:
        return sm.solve(conn,data_dict['filename'],data_dict['solver'])


@router.post('/get-upload-url')
async def get_upload_url(data_dict:dict,request:Request):
    with sqlConnect() as conn:
        return sm.get_upload_url(data_dict['filename'])
        