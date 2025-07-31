
from fastapi import FastAPI
from api.v1 import message
# from app.core.config import Settings

app = FastAPI()
app.include_router(message.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello World"}