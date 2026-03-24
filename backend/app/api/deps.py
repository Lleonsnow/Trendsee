from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from redis.asyncio import Redis

from app.core.security import decode_access_token
from app.db.session import get_session
from app.services.posts_service import PostsService
from sqlalchemy.ext.asyncio import AsyncSession

bearer_scheme = HTTPBearer(auto_error=False)


def get_redis(request: Request) -> Redis:
    redis = request.app.state.redis_client
    if redis is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Redis не доступен')
    return redis


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> int:
    if credentials is None or credentials.scheme.lower() != 'bearer':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Требуется авторизация',
        )
    token = credentials.credentials.strip()
    try:
        return decode_access_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректный токен')

async def get_posts_service(
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_session),
) -> PostsService:
    return PostsService(redis=redis, session=session)

