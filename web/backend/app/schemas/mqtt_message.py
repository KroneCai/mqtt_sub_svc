from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MQTTMessageSchema(BaseModel):
    ts: datetime
    topic: str
    t_factory: str
    t_product: str
    t_device_type: str
    t_device_id: str
    qos: int
    client_id: str
    msg_type: str
    msg_ts: datetime
    msg_temp: int
    msg_csq: str
    msg_bat: int
    msg_ccid: str
    msg_com: str
    msg_crc: str
    msg_version: str
    msg_side: int
    msg_triggle_time: datetime
    msg_cnt_L: int
    msg_cnt_R: int
    msg_T_state: int
    msg_time: str

    model_config = ConfigDict(from_attributes=True)

'''
class MQTTMessage(BaseModel):
    ts: datetime
    topic: str
    t_factory: str
    t_product: str
    t_device_type: str
    t_device_id: str
    qos: int
    payload_encrypted: bytes
    payload_decrypted: dict
    client_id: str
    msg_type: str
    msg_ts: datetime
    msg_temp: int
    msg_csq: str
    msg_bat: int
    msg_ccid: str
    msg_com: str
    msg_crc: str
    msg_version: str
    msg_side: int
    msg_triggle_time: datetime
    msg_cnt_L: int
    msg_cnt_R: int
    msg_T_state: int
    msg_time: str

    model_config = ConfigDict(from_attributes=True)
'''