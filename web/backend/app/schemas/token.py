from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TokenUserSchema(BaseModel):
    user_id: str
    user_name: str
    user_email: str
    tenant_code: str
    user_roles: list[str]
    model_config = ConfigDict(from_attributes=True)
    
class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    user: TokenUserSchema
    model_config = ConfigDict(from_attributes=True)

class TokenPayloadSchema(BaseModel):
    sub: str
    exp: int
    type: str

class TokenRefreshRequestSchema(BaseModel):
    token_type: str
    token: str
    user_name: str

class TokenRefreshResponseSchema(BaseModel):
    access_token: str
    refresh_token: str