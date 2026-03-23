from app.core.security import create_access_token
from app.db.models import User
from app.repositories.user_repo import create_user as repo_create_user
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user_and_token(session: AsyncSession, name: str) -> tuple[User, str]:
    user = await repo_create_user(session, name)
    token = create_access_token(user.id)
    return user, token

