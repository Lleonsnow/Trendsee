from fastapi import FastAPI
from redis.asyncio import Redis

from app.api.routes.posts import router as posts_router
from app.api.routes.users import router as users_router
from app.core.config import settings
from app.db.models import Base
from app.db.session import engine as db_engine


def create_app() -> FastAPI:
    app = FastAPI(title='Trendsee API')

    app.include_router(users_router)
    app.include_router(posts_router)

    @app.get('/health')
    async def health() -> dict:
        return {'ok': True}

    return app


app = create_app()


@app.on_event('startup')
async def on_startup() -> None:
    # Redis init
    app.state.redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=False)
    await app.state.redis_client.ping()

    # DB init (no migrations for this task)
    async with db_engine.begin() as conn:  # type: ignore[attr-defined]
        await conn.run_sync(Base.metadata.create_all)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    redis: Redis | None = getattr(app.state, 'redis_client', None)
    if redis is not None:
        await redis.close()

