from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://bartek:0000@localhost:3306/premier_league"
    database_host: str = "localhost"
    database_port: int = 3306
    database_user: str = "bartek"
    database_password: str = "0000"
    database_name: str = "premier_league"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()