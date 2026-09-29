from datetime import datetime, timedelta, timezone
import jwt
from jwt import InvalidTokenError
from fastapi import HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash
from .config import settings

ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)

def create_access_token(user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "exp": expires}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)

def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (InvalidTokenError, KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        ) from exc
