from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from config import settings
from loguru import logger
from model.model import Base

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
            Session = scoped_session(sessionmaker(bind=engine))
            return Session()
        except Exception as e:
            logger.error('Error getting Database Session:', e)
        return None
    