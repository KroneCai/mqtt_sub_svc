from sqlalchemy import Column, TEXT, INT, TIMESTAMP, LargeBinary, VARCHAR
from db.base import Base

class Tenant(Base):
    __tablename__ = 'tbl_tenant'
    code = Column('code', VARCHAR(32), primary_key=True)
    name = Column('name', VARCHAR(32))
    description = Column('description', TEXT)
    account = Column('account', VARCHAR(128))
    create_time = Column('create_time', TIMESTAMP)
    update_time = Column('update_time', TIMESTAMP)