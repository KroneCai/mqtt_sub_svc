from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LoginRequestSchema(BaseModel):
    user_id: str
    password: str
    tenant_code: str
    
    model_config = ConfigDict(from_attributes=True)
