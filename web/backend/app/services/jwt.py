from datetime import datetime, timedelta, timezone
from typing import Optional
from schemas.token import TokenUserSchema, TokenSchema, TokenPayloadSchema
from fastapi import FastAPI, Depends, HTTPException, status, Header
from jose import JWTError, jwt
from core.config import settings
from loguru import logger
from functools import lru_cache

# 用于签名的密钥，务必保密！生产环境应从环境变量读取。
ACCESS_TOKEN_SECRET_KEY = settings.ACCESS_TOKEN_SECRET_KEY
REFRESH_TOKEN_SECRET_KEY = settings.REFRESH_TOKEN_SECRET_KEY
# 使用的加密算法
ALGORITHM = "HS256"
# Token 的过期时间
ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRE
REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRE

def get_token_response(user: TokenUserSchema):
    """获取 Token 响应"""
    access_token, refresh_token = create_tokens(user.user_name)
    token_response = TokenSchema(
        access_token=access_token, 
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE,
        refresh_token=refresh_token,
        user=user
        )
    return token_response

def create_tokens(username: str):
    """创建 JWT Access Token & Refresh Token"""
    access_token_expires = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE)
    refresh_token_expires = datetime.now(timezone.utc) + timedelta(seconds=REFRESH_TOKEN_EXPIRE)
    
    access_token = jwt.encode(
        {"sub": username, "exp": access_token_expires, "type": "access token"}, 
        ACCESS_TOKEN_SECRET_KEY, 
        algorithm=ALGORITHM
        )
    refresh_token = jwt.encode(
        {"sub": username, "exp": refresh_token_expires, "type": "refresh token"}, 
        REFRESH_TOKEN_SECRET_KEY, 
        algorithm=ALGORITHM
        )
    
    return access_token, refresh_token

def verify_token(token_type: str, token:str, user_name: str):
    """验证 JWT Token"""
    # 从token中获取用户信息， 包括sub, exp, type。目标格式为：{"sub": username, "exp": refresh_token_expires, "type": "refresh token"}
    # 1.2 验证type是否为refresh token
    # 1.3 验证exp是否过期
    # 1.4 验证sub中用户名是否为空

    # 根据token type获取对应的secret key
    if token_type == "access token":
        secret_key = ACCESS_TOKEN_SECRET_KEY
    elif token_type == "refresh token":
        secret_key = REFRESH_TOKEN_SECRET_KEY
    else:
        raise HTTPException(status_code=400, detail="Invalid token type")
    try:
        # 解码token
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        
        # 验证token中的用户名是否为空
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # 验证token中的用户名是否与请求中的用户名一致
        if username.strip().lower() != user_name.strip().lower():
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # 验证token中的type是否与请求中的type一致
        token_type: str = payload.get("type")
        if token_type != token_type:
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        # 验证token中的exp是否过期
        exp: datetime = payload.get("exp")
        exp_datetime = datetime.fromtimestamp(exp, timezone.utc)
        if exp_datetime < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")
        
        # 返回结果
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 以下实现Token的验证函数
# 1. 带缓存的Token验证
@lru_cache(maxsize=1024)
def decode_token_cached(token: str) -> TokenPayloadSchema:
    """
    带缓存的Token解码函数
    缓存已验证的Token避免重复解密
    """
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayloadSchema(**payload)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# 2. 验证Token是否过期
def check_token_expiry(token_data: TokenPayloadSchema) -> bool:
    """检查Token是否过期"""
    current_datetime = datetime.now(timezone.utc)
    exp_datetime = datetime.fromtimestamp(token_data.exp,timezone.utc)
    return exp_datetime < current_datetime

# 3. 组合验证流程
async def verify_jwt_token(authorization: str = Header(...)) -> TokenPayloadSchema:
    """
    完整的JWT验证流程：
    1. 提取Token
    2. 使用缓存解码
    3. 检查过期时间
    """
    logger.info(authorization)
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )
    
    token = authorization.split(" ")[1]
    token_data = decode_token_cached(token)
    
    if check_token_expiry(token_data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    
    return token_data
