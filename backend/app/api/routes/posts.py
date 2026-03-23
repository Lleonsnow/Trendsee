from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.api.deps import get_current_user_id, get_posts_service
from app.schemas.post import (
    PostsFeedResponse,
    PostCreateRequest,
    PostResponse,
    PostUpdateRequest,
)

router = APIRouter(prefix='/posts', tags=['posts'])


@router.post('', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    req: PostCreateRequest,
    current_user_id: int = Depends(get_current_user_id),
    service=Depends(get_posts_service),
) -> PostResponse:
    try:
        post = await service.create_post_for_me(user_id=current_user_id, title=req.title, text=req.text)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return PostResponse(
        id=post.id,
        user_id=post.user_id,
        title=post.title,
        text=post.text,
        created_at=post.created_at.isoformat(),
        updated_at=post.updated_at.isoformat(),
    )


@router.patch('/{post_id}', response_model=PostResponse)
async def update_post(
    post_id: int,
    req: PostUpdateRequest,
    current_user_id: int = Depends(get_current_user_id),
    service=Depends(get_posts_service),
) -> PostResponse:
    try:
        updated = await service.update_post_for_me(
            user_id=current_user_id,
            post_id=post_id,
            title=req.title,
            text=req.text,
        )
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет прав')

    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пост не найден')

    return PostResponse(
        id=updated.id,
        user_id=updated.user_id,
        title=updated.title,
        text=updated.text,
        created_at=updated.created_at.isoformat(),
        updated_at=updated.updated_at.isoformat(),
    )


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user_id: int = Depends(get_current_user_id),
    service=Depends(get_posts_service),
) -> Response:
    try:
        deleted = await service.delete_post_for_me(user_id=current_user_id, post_id=post_id)
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет прав')

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пост не найден')

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/me', response_model=PostsFeedResponse)
async def get_my_posts(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    current_user_id: int = Depends(get_current_user_id),
    service=Depends(get_posts_service),
) -> PostsFeedResponse:
    result = await service.get_my_posts(user_id=current_user_id, offset=offset, limit=limit)
    return PostsFeedResponse(**result)


@router.get('/{user_id}', response_model=PostsFeedResponse)
async def get_posts_for_user(
    user_id: int,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    current_user_id: int = Depends(get_current_user_id),
    service=Depends(get_posts_service),
) -> PostsFeedResponse:
    if current_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет прав')

    result = await service.get_my_posts(user_id=user_id, offset=offset, limit=limit)
    return PostsFeedResponse(**result)

