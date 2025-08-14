from sqlalchemy import Column, TEXT, INT, TIMESTAMP, LargeBinary, VARCHAR, FLOAT
from db.base import Base

class Device(Base):
    __tablename__ = 'tbl_device'
    device_id = Column('device_id', VARCHAR(32), primary_key=True)
    device_type = Column('device_type', VARCHAR(32))
    factory = Column('factory', VARCHAR(32))
    product = Column('product', VARCHAR(32))
    tenant = Column('tenant', VARCHAR(32))
    site = Column('site', VARCHAR(32))
    area = Column('area', VARCHAR(32))
    seq = Column('seq', VARCHAR(32))
    longitude = Column('longitude', FLOAT)
    latitude = Column('latitude', FLOAT)
    status = Column('status', VARCHAR(32))
    deployment_date = Column('deployment_date', TIMESTAMP)