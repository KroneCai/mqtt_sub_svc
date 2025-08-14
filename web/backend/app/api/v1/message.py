from fastapi import APIRouter, Depends, HTTPException
from schemas.mqtt_message import MQTTMessage
from crud.mqtt_message import get_message_by_device_id
from sqlalchemy.orm import Session
from db.db import Database
from loguru import logger

router = APIRouter()

def get_db():
    db = Database()
    engine = db.get_db_connection()
    session = db.get_db_session(engine)
    return session

@router.get("/message/{deviceId}", response_model=list[MQTTMessage])
async def get_mqtt_message(deviceId: str):
    db_messages = get_message_by_device_id(get_db(), device_id=deviceId)
    if db_messages is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_messages
    
