from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_redis
from app.db.session import get_session
from app.services.posts_service import feed_cache_key
from app.repositories.user_repo import delete_user, get_user_by_id, update_user_name
from app.schemas.user import UserCreateRequest, UserResponse, UserTokenResponse, UserUpdateRequest
from app.services.auth_service import create_user_and_token

router = APIRouter(prefix='/users', tags=['users'])


@router.post('', response_model=UserTokenResponse, status_code=status.HTTP_201_CREATED)
async def create_user(req: UserCreateRequest, session: AsyncSession = Depends(get_session)) -> UserTokenResponse:
    user, token = await create_user_and_token(session, name=req.name)
    return UserTokenResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            name=user.name,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
        ),
    )


@router.get('/{user_id}/token', response_model=UserTokenResponse)
async def get_user_token(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> UserTokenResponse:
    user = await get_user_by_id(session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

    from app.core.security import create_access_token

    token = create_access_token(user.id)
    return UserTokenResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            name=user.name,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
        ),
    )


@router.patch('/{user_id}', response_model=UserResponse)
async def update_user(
    user_id: int,
    req: UserUpdateRequest,
    session: AsyncSession = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
) -> UserResponse:
    if current_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет прав')

    user = await update_user_name(session, user_id=user_id, name=req.name)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

    return UserResponse(
        id=user.id,
        name=user.name,
        created_at=user.created_at.isoformat(),
        updated_at=user.updated_at.isoformat(),
    )


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
    redis=Depends(get_redis),
) -> Response:
    if current_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет прав')

    deleted = await delete_user(session, user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

    await redis.delete(feed_cache_key(user_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

