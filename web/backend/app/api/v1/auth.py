from math import atan
from fastapi import APIRouter, Depends, HTTPException
from schemas.login import LoginRequestSchema
from schemas.token import TokenPayloadSchema, TokenSchema, TokenUserSchema, TokenRefreshRequestSchema, TokenRefreshResponseSchema
from services.jwt import get_token_response, create_tokens, verify_token
from crud.user import login
from sqlalchemy.orm import Session
from db.db import Database
from loguru import logger
from services.jwt import verify_jwt_token

router = APIRouter()

def get_db():
    db = Database()
    engine = db.get_db_connection()
    session = db.get_db_session(engine)
    return session

sessionLocal = get_db()

# 登录接口
# 输入参数包括：user_id, password, tenant_code
# 输出参数包括：token, userId, tenantCode, userName, userEmail, userRoles
# 其中：
# 1. token是JWT格式的字符串，代表用户的登录凭证
# 2. userId是一个字符串，代表用户的ID，例如："123456"
# 3. tenantCode是一个字符串，代表用户的租户代码，例如："tenant1"
# 4. userName是一个字符串，代表用户的姓名，例如："admin"
# 5. userEmail是一个字符串，代表用户的邮箱，例如："admin@example.com"
# 6. userRoles是一个列表，每个元素是一个字符串，代表用户的角色，例如：["admin", "user"]

@router.post("/token",response_model=TokenSchema)
async def login_to_get_token(loginRequest: LoginRequestSchema):
    try:
        # 详细记录请求数据
        logger.info(f"登录请求开始处理 - 用户ID: {loginRequest.user_id}, 租户代码: {loginRequest.tenant_code}")
        logger.debug(f"完整登录请求数据: {loginRequest.model_dump_json()}")
        
        # 验证请求数据
        if not loginRequest.user_id or not loginRequest.user_id.strip():
            logger.warning("登录失败 - 用户ID为空")
            raise HTTPException(status_code=422, detail="用户ID不能为空")
        
        if not loginRequest.password or not loginRequest.password.strip():
            logger.warning("登录失败 - 密码为空")
            raise HTTPException(status_code=422, detail="密码不能为空")
            
        if not loginRequest.tenant_code or not loginRequest.tenant_code.strip():
            logger.warning("登录失败 - 租户代码为空")
            raise HTTPException(status_code=422, detail="租户代码不能为空")
        
        # 尝试登录
        db_user = login(db=sessionLocal, 
                       user_id=loginRequest.user_id, 
                       password=loginRequest.password,
                       tenant_code=loginRequest.tenant_code)
        
        # 处理登录结果
        if db_user is None:
            logger.warning(f"登录失败 - 用户不存在或密码错误 - 用户ID: {loginRequest.user_id}, 租户代码: {loginRequest.tenant_code}")
            raise HTTPException(status_code=401, detail="用户不存在或密码错误")
        
        # 登录成功
        logger.info(f"登录成功 - 用户ID: {loginRequest.user_id}, 租户代码: {loginRequest.tenant_code}")
        # 生成JWT token
        token_user = TokenUserSchema(
            user_id=db_user.user_id,
            user_name=db_user.user_name,
            user_email=db_user.user_email,
            tenant_code=db_user.tenant_code,
            user_roles=db_user.user_roles
        )
        token_response = get_token_response(token_user)
        return token_response
        
    except HTTPException:
        # 重新抛出HTTP异常，保持原始状态码和详情
        raise
    except Exception as e:
        # 捕获并记录其他未预期的异常
        logger.error(f"登录过程中发生未预期异常: {str(e)}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail="服务器内部错误")

@router.post("/refresh",response_model=TokenRefreshResponseSchema)
async def refresh_token(refreshRequest: TokenRefreshRequestSchema):
    # 1. 验证refresh token
    username = verify_token(token_type=refreshRequest.token_type,token=refreshRequest.token,user_name=refreshRequest.user_name)
    # 2. 调用services.jwt.create_tokens生成新的access token和refresh token并返回
    try:
        accessToken, refreshToken = create_tokens(username)
        token_response = TokenRefreshResponseSchema(
            access_token = accessToken,
            refresh_token= refreshToken
        )
        return token_response
    except HTTPException:
        # 重新抛出HTTP异常，保持原始状态码和详情
        raise
    except Exception as e:
        # 捕获并记录其他未预期的异常
        logger.error(f"刷新token过程中发生未预期异常: {str(e)}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail="服务器内部错误")

@router.get('/verify', response_model=TokenPayloadSchema)
async def verify_a_token(payload: TokenPayloadSchema = Depends(verify_jwt_token)):
    return payload
