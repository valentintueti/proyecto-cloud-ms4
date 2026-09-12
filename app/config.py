from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MS1_BASE_URL: str
    MS2_BASE_URL: str
    MS3_BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()