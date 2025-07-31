from pydantic import BaseModel

class Message(BaseModel):
    deviceId: str
    payload: str
