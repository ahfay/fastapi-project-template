from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    test_api: str
    db_url: str


    class Config:
        env_file = ".env"

settings = AppConfig()

