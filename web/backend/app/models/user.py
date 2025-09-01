from sqlalchemy import Column, TEXT, INT, TIMESTAMP, LargeBinary, VARCHAR, FLOAT
from db.base import Base

class UserModel(Base):
    __tablename__ = 'tbl_user'
    user_id = Column('user_id', VARCHAR(64), primary_key=True)
    user_name = Column('user_name', VARCHAR(32))
    user_email = Column('user_email', VARCHAR(64))
    tenant_code = Column('tenant_code', VARCHAR(32))
    password = Column('password', VARCHAR(64))
    salt = Column('salt', VARCHAR(32))
    user_roles = Column('user_roles', VARCHAR(128))
    status = Column('status', VARCHAR(32))
    last_login_time = Column('last_login_time', TIMESTAMP)
    fail_login_count = Column('fail_login_count', INT)
    last_login_ip = Column('last_login_ip', VARCHAR(39))
    create_time = Column('create_time', TIMESTAMP)
    update_time = Column('update_time', TIMESTAMP)