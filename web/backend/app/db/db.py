from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from core.config import settings
from loguru import logger
from db.base import Base
# 在调用 create_all() 的脚本中显式导入所有模型文件（即使未直接使用）
from models.tenant import TenantModel
from models.user import UserModel
from models.device import DeviceModel
from models.mqtt_message import MQTTMessageModel
from models.ref import ReferenceModel
from models.mqtt_log import MQTTLogModel

class Database():
    
    def __init__(self) -> None:
        self.connection_is_active = False
        self.engine = None
    
    def get_db_connection(self):
        if self.connection_is_active == False:
            try:
                self.engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
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
    