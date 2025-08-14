from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Reference(BaseModel):
    id: int
    namespace: str
    description: str
    seq: int
    key: str
    value: str
    create_time: datetime
    update_time: datetime
    model_config = ConfigDict(from_attributes=True)