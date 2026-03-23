from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    payload = {
        'sub': str(user_id),
        'iat': int(now.timestamp()),
        'exp': int(exp.timestamp()),
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        sub = payload.get('sub')
        if not isinstance(sub, str) or not sub.isdigit():
            raise JWTError('Некорректный sub')
        return int(sub)
    except JWTError as e:
        raise JWTError('Некорректный или истёкший токен') from e

