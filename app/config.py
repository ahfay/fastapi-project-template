from pydantic_settings import BaseSettings
from typing import ClassVar
from pytz import timezone

class AppConfig(BaseSettings):
    TEST_API: str
    DB_URL: str
    TIMEZONE: ClassVar[timezone] = timezone("Asia/Jakarta")


    class Config:
        env_file = ".env"

settings = AppConfig()

