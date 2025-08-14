from sqlalchemy.orm import Session
from loguru import logger
from models.mqtt_message import MQTTMessage

def get_message_by_device_id(db: Session, device_id: str):
    # data = []
    # logger.info(f"get_message_by_device_id device_id: {device_id}")
    return db.query(MQTTMessage).filter(MQTTMessage.t_device_id == device_id).order_by(MQTTMessage.ts.desc()).all()

def get_message_by_msg_type(db: Session, msg_type: str):
    return db.query(MQTTMessage).filter(MQTTMessage.msg_type == msg_type).order_by(MQTTMessage.ts.desc()).all()

def get_message_by_msg_type_and_device_id(db: Session, msg_type: str, device_id: str):
    return db.query(MQTTMessage).filter(MQTTMessage.msg_type == msg_type, MQTTMessage.t_device_id == device_id).order_by(MQTTMessage.ts.desc()).all()
