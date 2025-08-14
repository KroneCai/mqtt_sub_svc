from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Device(BaseModel):
    device_id: str
    device_type: str
    factory: str
    product: str
    tenant: str
    site: str
    area: str
    seq: str
    longitude: float
    latitude: float
    status: str
    deployment_date: datetime
    
    model_config = ConfigDict(from_attributes=True)

'''
    device_id = Column('device_id', VARCHAR(32), primary_key=True)
    device_type = Column('device_type', VARCHAR(32))
    factory = Column('factory', VARCHAR(32))
    product = Column('product', VARCHAR(32))
    tenant = Column('tenant', VARCHAR(32))
    site = Column('site', VARCHAR(32))
    area = Column('area', VARCHAR(32))
    seq = Column('seq', VARCHAR(32))
    longitude = Column('longitude', float)
    latitude = Column('latitude', float)
    status = Column('status', VARCHAR(32))
    deployment_date = Column('deployment_date', TIMESTAMP)
'''
