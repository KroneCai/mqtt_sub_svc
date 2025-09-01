from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class TenantSchema(BaseModel):
    code: str
    name: str
    description: str
    account: str
    create_time: datetime
    update_time: datetime
    
    model_config = ConfigDict(from_attributes=True)