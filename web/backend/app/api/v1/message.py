from fastapi import APIRouter
from schemas.message import Message

router = APIRouter()

@router.get("/message/{deviceId}", response_model=Message)
async def get_message(deviceId: str):
    return Message(deviceId=deviceId, payload="Hello World!!")
