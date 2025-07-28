from db.db import Database
from model.model import MQTTLog 
from datetime import datetime
from loguru import logger

class Logger:
    def __init__(self):
        self.db = Database()
        self.engine = self.db.get_db_connection()
        self.session = self.db.get_db_session(self.engine)

    def add_log(self,level, message):
        try:
            log = MQTTLog(ts=datetime.now(),
                          level=level,
                          message=message)
            self.session.add(log)
            self.session.commit()
        except Exception as e:
            logger.error(f'Failed to add log: {e}')
    