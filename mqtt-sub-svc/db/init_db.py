from sqlalchemy import create_engine
from config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

result = ""

try:
    engine.connect()
    result = "Connected"
except Exception as e:
    result = e
finally:
    engine.dispose()
    result += "disposed"


#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()