from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Application settings
    """

    API_KEY: str
    API_SECRET: str
    PHONE_NUMBER: str

    class Config:
        env_file = ".env"


settings = Settings()
