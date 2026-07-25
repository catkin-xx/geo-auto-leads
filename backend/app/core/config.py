from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    
    # 项目基本信息
    PROJECT_NAME: str = "GEO Auto Leads"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    
    # 数据库
    DATABASE_URL: str = "postgresql://geo_user:geo_pass@db:5432/geo_auto"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # 地图API密钥
    AMAP_KEY: Optional[str] = None
    BAIDU_MAP_KEY: Optional[str] = None
    
    # 企业微信
    WECOM_CORP_ID: Optional[str] = None
    WECOM_CORP_SECRET: Optional[str] = None
    
    # 短信
    SMS_ACCESS_KEY: Optional[str] = None
    SMS_ACCESS_SECRET: Optional[str] = None
    
    # 安全
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()