from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = 'sqlite:///./anchor.db'
    secret_key: str = 'anchor-super-secret-key-change-in-production-min-32-chars'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 1440
    frontend_url: str = 'http://localhost:3000'

    class Config:
        env_file = '.env'

settings = Settings()