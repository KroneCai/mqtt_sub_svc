from sqlalchemy import Column, TEXT, INT, TIMESTAMP, LargeBinary, VARCHAR
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from db.base import Base

# Base = declarative_base()

class MQTTLog(Base):
    __tablename__ = 'tbl_mqtt_log'
    ts = Column('ts', TIMESTAMP, primary_key=True)
    level = Column('level', VARCHAR(10))
    message = Column('message', TEXT)