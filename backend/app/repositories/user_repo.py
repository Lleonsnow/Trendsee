from datetime import timezone

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, utcnow


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def create_user(session: AsyncSession, name: str) -> User:
    user = User(name=name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user_name(session: AsyncSession, user_id: int, name: str) -> User | None:
    user = await get_user_by_id(session, user_id)
    if user is None:
        return None

    user.name = name
    user.updated_at = utcnow()
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    stmt = delete(User).where(User.id == user_id)
    res = await session.execute(stmt)
    await session.commit()
    return res.rowcount is not None and res.rowcount > 0

