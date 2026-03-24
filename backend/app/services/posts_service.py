import asyncio
import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models import Post
from app.repositories.posts_repo import (
    create_post,
    delete_post,
    get_all_posts_for_user_for_cache,
    get_post_by_id,
    get_posts_for_user,
    update_post,
)


def _post_to_response(post: Post) -> dict:
    return {
        'id': post.id,
        'user_id': post.user_id,
        'title': post.title,
        'text': post.text,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
    }


def feed_cache_key(user_id: int) -> str:
    return f'trendsee:feed:{user_id}'


class PostsService:
    def __init__(self, *, redis, session: AsyncSession):
        self._redis = redis
        self._session = session

    async def _rebuild_feed_cache(self, *, user_id: int) -> None:
        posts = await get_all_posts_for_user_for_cache(self._session, user_id=user_id)
        payload = {
            'total': len(posts),
            'items': [_post_to_response(p) for p in posts],
        }
        await self._redis.set(
            feed_cache_key(user_id),
            json.dumps(payload, ensure_ascii=False),
            ex=settings.HOT_FEED_TTL_SECONDS,
        )

    async def get_my_posts(self, *, user_id: int, offset: int, limit: int) -> dict:
        cached_raw = await self._redis.get(feed_cache_key(user_id))
        if cached_raw is not None:
            cached = json.loads(cached_raw)
            total = int(cached.get('total', 0))
            items_all = cached.get('items', [])
            items_slice = items_all[offset : offset + limit]
            return {
                'items': items_slice,
                'total': total,
                'has_more': offset + limit < total,
            }

        await asyncio.sleep(settings.POSTS_PG_DELAY_SECONDS)

        items, total = await get_posts_for_user(
            self._session,
            user_id=user_id,
            offset=offset,
            limit=limit,
        )
        await self._rebuild_feed_cache(user_id=user_id)
        return {
            'items': [_post_to_response(p) for p in items],
            'total': total,
            'has_more': offset + limit < total,
        }

    async def create_post_for_me(self, *, user_id: int, title: str, text: str) -> Post:
        post = await create_post(self._session, user_id=user_id, title=title, text=text)
        await self._rebuild_feed_cache(user_id=user_id)
        return post

    async def update_post_for_me(
        self,
        *,
        user_id: int,
        post_id: int,
        title: str | None,
        text: str | None,
    ) -> Post | None:
        post = await get_post_by_id(self._session, post_id=post_id)
        if post is None:
            return None
        if post.user_id != user_id:
            # У маршрута это превратится в 403
            raise PermissionError('Попытка изменить чужой пост')

        updated = await update_post(
            self._session,
            post_id,
            title=title,
            text=text,
        )
        await self._rebuild_feed_cache(user_id=user_id)
        return updated

    async def delete_post_for_me(self, *, user_id: int, post_id: int) -> bool:
        post = await get_post_by_id(self._session, post_id=post_id)
        if post is None:
            return False
        if post.user_id != user_id:
            raise PermissionError('Попытка удалить чужой пост')

        deleted = await delete_post(self._session, post_id=post_id)
        if deleted:
            await self._rebuild_feed_cache(user_id=user_id)
        return deleted

