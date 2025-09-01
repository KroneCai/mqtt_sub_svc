from sqlalchemy.orm import Session
from loguru import logger
from models.mqtt_message import MQTTMessageModel

def get_message_by_device_id(db: Session, device_id: str):
    # data = []
    # logger.info(f"get_message_by_device_id device_id: {device_id}")
    return db.query(MQTTMessageModel).filter(MQTTMessageModel.t_device_id == device_id).order_by(MQTTMessageModel.ts.desc()).all()

def get_message_by_msg_type(db: Session, msg_type: str):
    return db.query(MQTTMessageModel).filter(MQTTMessageModel.msg_type == msg_type).order_by(MQTTMessageModel.ts.desc()).all()

def get_message_by_msg_type_and_device_id(db: Session, msg_type: str, device_id: str):
    return db.query(MQTTMessageModel).filter(MQTTMessageModel.msg_type == msg_type, MQTTMessageModel.t_device_id == device_id).order_by(MQTTMessageModel.ts.desc()).all()
