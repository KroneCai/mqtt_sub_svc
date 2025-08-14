from fastapi import FastAPI
import core.config as config
from api.v1 import message
from api.v1 import tenant
from api.v1 import device
    
app = FastAPI(title=config.APP_NAME)
app.include_router(message.router, prefix="/api/v1")
app.include_router(tenant.router, prefix="/api/v1")
app.include_router(device.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}