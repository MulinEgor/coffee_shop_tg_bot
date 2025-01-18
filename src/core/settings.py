from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс для хранения настроек из .env файла.
    """
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    bot_token: str
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    class Config:
        env_file = ".env"
        extra = "ignore" 


settings = Settings()
