from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # 系统配置
    APP_NAME: str = "MQTT Web Server"
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI:str = "postgresql+psycopg2://kronecai@localhost:5432/mqtt_db"
    
    # JWT安全配置
    ACCESS_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE: int = 3600  # 1小时
    REFRESH_TOKEN_EXPIRE: int = 604800  # 7天
    
    # 环境标志
    ENV: str = "dev"  # dev/test/prod
    
    class Config:
        env_file = Path(__file__).parent.parent.parent / "env" / ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False  # 不区分大小写

# 单例模式初始化
settings = Settings()