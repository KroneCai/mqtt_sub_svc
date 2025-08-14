from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, Session, scoped_session
import core.config as config
from loguru import logger
from db.base import Base
# 在调用 create_all() 的脚本中显式导入所有模型文件（即使未直接使用）
from models.tenant import Tenant
from models.device import Device
from models.mqtt_message import MQTTMessage
from models.ref import Reference
from models.mqtt_log import MQTTLog

class Database():
    
    def __init__(self) -> None:
        self.connection_is_active = False
        self.engine = None
    
    def get_db_connection(self):
        if self.connection_is_active == False:
            try:
                self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
                Base.metadata.create_all(self.engine)
                return self.engine
            except Exception as e:
                logger.error("Error connection to PostgreSQL Database: ", e)
        return self.engine
    
    ### return active session
    def get_db_session(self, engine):
        try:
            session = scoped_session(sessionmaker(bind=engine))
            return session
        except Exception as e:
            logger.error('Error getting Database Session:', e)
        return None
    