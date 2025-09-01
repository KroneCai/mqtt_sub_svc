from pydantic import BaseModel, ConfigDict
from datetime import datetime

class DeviceSchema(BaseModel):
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

