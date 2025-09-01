from fastapi import FastAPI
from core.config import settings
from api.v1 import message
from api.v1 import tenant
from api.v1 import device
from api.v1 import user
from api.v1 import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.APP_NAME)
app.include_router(message.router, prefix="/api/v1")
app.include_router(tenant.router, prefix="/api/v1")
app.include_router(device.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
