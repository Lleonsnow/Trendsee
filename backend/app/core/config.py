from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql+asyncpg://trendsee:trendsee@postgres:5432/trendsee'
    REDIS_URL: str = 'redis://redis:6379/0'

    JWT_SECRET: str = 'change_me'
    JWT_ALG: str = 'HS256'
    JWT_EXPIRE_MINUTES: int = 720

    HOT_FEED_TTL_SECONDS: int = 600
    POSTS_PG_DELAY_SECONDS: float = 2.0


settings = Settings()

