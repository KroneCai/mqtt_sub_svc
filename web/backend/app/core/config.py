from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MQTT Web Server"
    sqlalchemy_database_url: str = "postgresql+psycopg2://kronecai@localhost:5432/mqtt_db"
    jwt_secret: str = "your-secret-key"
