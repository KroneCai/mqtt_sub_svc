from sqlalchemy.orm import Session
from loguru import logger
from models.device import DeviceModel

def get_device_by_device_id(db: Session, device_id: str):
    # data = []
    logger.info(f"get_device_by_device_id device_id: {device_id}")
    result = db.query(DeviceModel).filter(DeviceModel.device_id == device_id).order_by(DeviceModel.deployment_date.desc()).all()
    return result

def get_devices_by_tenant_code(db: Session, tenant_code: str):
    # data = []
    logger.info(f"get_devices_by_tenant_code tenant_code: {tenant_code}")
    result = db.query(DeviceModel).filter(DeviceModel.tenant_code == tenant_code).order_by(DeviceModel.deployment_date.desc()).all()
    return result

def get_devices(db: Session, tenant_code: str):
    return db.query(DeviceModel).where(DeviceModel.tenant == tenant_code).order_by(DeviceModel.deployment_date.desc()).all()

def create_device(db: Session, device: DeviceModel):
    device_orm = DeviceModel(**device.model_dump())
    db.add(device_orm)
    db.commit()
    db.refresh(device_orm)
    return device_orm

def update_device(db: Session, device: DeviceModel):
    device_orm = DeviceModel(**device.model_dump())
    db.merge(device_orm)
    db.commit()
    return device_orm

def delete_device(db: Session, device_id: str):
    device = db.query(DeviceModel).filter(DeviceModel.device_id == device_id).first()
    db.delete(device)
    db.commit()
    return device
