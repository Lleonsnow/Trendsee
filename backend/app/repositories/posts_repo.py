from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Post, utcnow


async def get_post_by_id(session: AsyncSession, post_id: int) -> Post | None:
    res = await session.execute(select(Post).where(Post.id == post_id))
    return res.scalar_one_or_none()


async def create_post(session: AsyncSession, user_id: int, title: str, text: str) -> Post:
    post = Post(user_id=user_id, title=title, text=text)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


async def update_post(
    session: AsyncSession,
    post_id: int,
    *,
    title: str | None,
    text: str | None,
) -> Post | None:
    post = await get_post_by_id(session, post_id)
    if post is None:
        return None

    if title is not None:
        post.title = title
    if text is not None:
        post.text = text
    post.updated_at = utcnow()

    await session.commit()
    await session.refresh(post)
    return post


async def delete_post(session: AsyncSession, post_id: int) -> bool:
    stmt = delete(Post).where(Post.id == post_id)
    res = await session.execute(stmt)
    await session.commit()
    return res.rowcount is not None and res.rowcount > 0


async def get_posts_for_user(
    session: AsyncSession,
    *,
    user_id: int,
    offset: int,
    limit: int,
) -> tuple[list[Post], int]:
    total = await session.scalar(
        select(func.count()).select_from(Post).where(Post.user_id == user_id),
    )
    items_res = await session.execute(
        select(Post)
        .where(Post.user_id == user_id)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit),
    )
    items = list(items_res.scalars().all())
    return items, int(total or 0)


async def get_all_posts_for_user_for_cache(
    session: AsyncSession,
    *,
    user_id: int,
) -> list[Post]:
    items_res = await session.execute(
        select(Post).where(Post.user_id == user_id).order_by(Post.created_at.desc()),
    )
    return list(items_res.scalars().all())

