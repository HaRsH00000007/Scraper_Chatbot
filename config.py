from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str
    DATABASE_NAME: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    DOMAIN_URL: str
    SECRET_KEY:str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int # Token expiry in minutes

    class Config:
        env_file = ".env"

settings = Settings()
