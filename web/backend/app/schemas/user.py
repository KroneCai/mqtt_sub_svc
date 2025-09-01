from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserSchema(BaseModel):
    user_id: str
    user_name: str
    user_email: str
    tenant_code: str
    password: str
    salt: str
    user_roles: list[str]
    status: str
    last_login_time: datetime
    fail_login_count: int
    last_login_ip: str
    create_time: datetime
    update_time: datetime
    
    model_config = ConfigDict(from_attributes=True)
