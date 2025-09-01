
from argparse import Namespace
from unicodedata import category
from sqlalchemy import Column, TEXT, INT, TIMESTAMP, LargeBinary, VARCHAR
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from db.base import Base

# Base = declarative_base()

class ReferenceModel(Base):
    __tablename__ = 'tbl_ref'
    id = Column('id', INT, primary_key=True)
    namespace = Column('namespace', VARCHAR(128))
    description = Column('description', TEXT)
    seq = Column('seq', INT)
    key = Column('key', VARCHAR(32))
    value = Column('value', VARCHAR(32))
    create_time = Column('create_time', TIMESTAMP)
    update_time = Column('update_time', TIMESTAMP)