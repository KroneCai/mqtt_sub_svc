from sqlalchemy import Column, TEXT, INT, TIMESTAMP, LargeBinary, VARCHAR
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from db.base import Base

# Base = declarative_base()

class MQTTMessageModel(Base):
    __tablename__ = 'tbl_mqtt_message'
    ts = Column('ts', TIMESTAMP, primary_key=True)
    topic  = Column('topic', VARCHAR(128))
    t_factory = Column('t_factory', VARCHAR(32))
    t_product = Column('t_product', VARCHAR(32))
    t_device_type = Column('t_device_type', VARCHAR(32))
    t_device_id = Column('t_device_id', VARCHAR(32), index=True)
    qos = Column('qos', INT)
    client_id  = Column('client_id', VARCHAR(16))
    msg_type = Column('msg_type', VARCHAR(16), index=True)
    msg_ts = Column('msg_ts', TIMESTAMP, index=True)
    msg_temp = Column('msg_temp', INT)
    msg_csq = Column('msg_csq', VARCHAR(16))
    msg_bat = Column('msg_bat', INT)
    msg_ccid = Column('msg_ccid', VARCHAR(32))
    msg_com = Column('msg_com', VARCHAR(16))
    msg_crc = Column('msg_crc', VARCHAR(16))
    msg_version = Column('msg_version', VARCHAR(16))
    msg_side = Column('msg_side', INT) # 触发侧：1-左侧触发；2-右侧触发
    msg_triggle_time = Column('msg_triggle_time', TIMESTAMP) # 首次触发时间
    msg_cnt_L = Column('msg_cnt_L', INT) # 左侧触发次数
    msg_cnt_R = Column('msg_cnt_R', INT) # 右侧触发次数
    msg_T_state = Column('msg_T_state', INT) # 高温报警及温度恢复故障类型 1-高温报警；0-温度恢复
    msg_time = Column('msg_time', VARCHAR(32)) # 时间
