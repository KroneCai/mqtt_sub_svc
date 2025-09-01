from sqlalchemy.orm import Session
from loguru import logger
from models.user import UserModel
import secrets
import hashlib
from typing import List
import json

def login(db: Session, user_id: str, password: str,tenant_code: str):
    user_orm = db.query(UserModel).filter(UserModel.user_id == user_id,UserModel.tenant_code == tenant_code).first()
    if user_orm is None:
        return None
    # 密码加盐加密，使用SHA-256算法加密
    salted_password = password + user_orm.salt
    encrypted_password = hashlib.sha256(salted_password.encode()).hexdigest()
    if user_orm.password != encrypted_password:
        return None
    # 转换 PostgreSQL 数组字符串为 Python 列表
    if user_orm and isinstance(user_orm.user_roles, str):
        user_orm.user_roles = convert_postgres_array_to_list(user_orm.user_roles)
    return user_orm

def get_user_by_user_id(db: Session, user_id: str,tenant_code: str):
    # data = []
    # logger.info(f"get_user_by_user_id user_id: {user_id} tenant_code: {tenant_code}")
    result = db.query(UserModel).filter(UserModel.user_id == user_id,UserModel.tenant_code == tenant_code).first()
    if result and isinstance(result.user_roles, str):
        result.user_roles = convert_postgres_array_to_list(result.user_roles)
    return result

def create_user(db: Session, user: UserModel):
    user_orm = UserModel(**user.model_dump())
    # 生成随机盐值
    user_orm.salt = secrets.token_hex(16)
    # 密码加盐加密，使用SHA-256算法加密
    salted_password = user_orm.password + user_orm.salt
    encrypted_password = hashlib.sha256(salted_password.encode()).hexdigest()
    
    user_orm.password = encrypted_password
    db.add(user_orm)
    db.commit()
    db.refresh(user_orm)
    return user_orm

def update_user(db: Session, user: UserModel):
    user_orm = UserModel(**user.model_dump())
    # 生成随机盐值
    user_orm.salt = secrets.token_hex(16)
    # 密码加盐加密，使用SHA-256算法加密
    salted_password = user_orm.password + user_orm.salt
    encrypted_password = hashlib.sha256(salted_password.encode()).hexdigest()

    user_orm.password = encrypted_password
    db.merge(user_orm)
    db.commit()
    return user_orm


def convert_postgres_array_to_list(array_str: str) -> List[str]:
    """
    将 PostgreSQL 数组字符串转换为 Python 列表
    示例: '{user,admin}' -> ['user', 'admin']
    """
    if not array_str or not isinstance(array_str, str):
        return []
    
    # 移除花括号并按逗号分割
    if array_str.startswith('{') and array_str.endswith('}'):
        cleaned = array_str[1:-1]
        return [item.strip() for item in cleaned.split(',') if item.strip()]
    
    # 如果是 JSON 字符串格式
    if array_str.startswith('[') and array_str.endswith(']'):
        try:
            return json.loads(array_str)
        except json.JSONDecodeError:
            pass
    
    # 如果是简单的逗号分隔字符串
    return [item.strip() for item in array_str.split(',') if item.strip()]