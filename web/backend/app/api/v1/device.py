from fastapi import APIRouter, Depends, HTTPException
from schemas.device import Device as DeviceSchema
from crud.device import get_devices, get_device_by_device_id, create_device, update_device, delete_device
from sqlalchemy.orm import Session
from db.db import Database
from loguru import logger

router = APIRouter()

def get_db():
    db = Database()
    engine = db.get_db_connection()
    session = db.get_db_session(engine)
    return session

sessionLocal = get_db()

@router.get("/devices/{tenantCode}", response_model=list[DeviceSchema])
async def get_device_list(tenantCode: str):
    devices = get_devices(db=sessionLocal, tenant_code=tenantCode)
    if devices == []:
        raise HTTPException(status_code=404, detail="Device not found")
    return devices

@router.get("/device/{deviceId}", response_model=DeviceSchema)
async def get_device(deviceId: str):
    devices = get_device_by_device_id(db=sessionLocal,  device_id=deviceId)
    if devices == []:
        raise HTTPException(status_code=404, detail="Device not found")
    return devices[0]

@router.post("/device", response_model=DeviceSchema)
async def new_device(device: DeviceSchema):
    db_device = get_device_by_device_id(db=sessionLocal, device_id=device.device_id) 
    if db_device != []:
        raise HTTPException(status_code=409, detail="Device already exists")
    logger.info(f"new_device device: {device}")
    create_device(sessionLocal, device)
    return DeviceSchema.model_validate(device)

@router.put("/device", response_model=DeviceSchema)
async def save_device(device: DeviceSchema):
    db_device = get_device_by_device_id(db=sessionLocal, device_id=device.device_id) 
    if db_device == []:
        raise HTTPException(status_code=404, detail="Device not found")
    update_device(db=sessionLocal, device=device)
    return DeviceSchema.model_validate(device)

@router.delete("/device/{deviceId}")
async def remove_device(deviceId: str):
    db_device = get_device_by_device_id(db=sessionLocal, device_id=deviceId) 
    if db_device == []:
        raise HTTPException(status_code=404, detail="Device not found")
    delete_device(db=sessionLocal, device_id=deviceId)
    return {"message": "Device deleted"}

