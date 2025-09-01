from math import atan
from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserSchema
from crud.user import get_user_by_user_id, create_user, update_user
from sqlalchemy.orm import Session
from db.db import Database
from loguru import logger

router = APIRouter()

def get_db():
    db = Database()
    engine = db.get_db_connection()
    session = db.get_db_session(engine)
    return session

sessionLocal = get_db()

@router.get("/user/{tenantCode}/{userId}", response_model=UserSchema)
async def get_user(tenantCode: str, userId: str):
    user = get_user_by_user_id(db=sessionLocal, user_id=userId,tenant_code=tenantCode)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/user", response_model=UserSchema)
async def new_user(user: UserSchema):
    db_user = get_user_by_user_id(db=sessionLocal, user_id=user.user_id,tenant_code=user.tenant_code) 
    if db_user != None:   
        raise HTTPException(status_code=409, detail="User already exists")
    logger.info(f"new_user user: {user}")
    create_user(sessionLocal, user)
    return UserSchema.model_validate(user)

@router.put("/user", response_model=UserSchema)
async def save_user(user: UserSchema):
    db_user = get_user_by_user_id(db=sessionLocal, user_id=user.user_id) 
    if db_user == []:
        raise HTTPException(status_code=404, detail="User not found")
    update_user(db=sessionLocal, user=user)
    return UserSchema.model_validate(user)
