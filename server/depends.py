from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from configs.config import secret, encrypt_algorithm

from vendors.db import async_session

from fastapi.exceptions import HTTPException

oauth2_scheme_account = OAuth2PasswordBearer(
    tokenUrl='/' + 'auth/login', auto_error=False
)


def get_access_token(self, life_time_days: int = 180) -> str:
    payload = {

        'sub': f"{self.id}",
        'exp': datetime.now() + timedelta(days=life_time_days),
        'is_email_confirmed': self.active
    }

    return jwt.encode(payload, secret, algorithm=encrypt_algorithm)


def get_payload_from_token(token: str = Depends(oauth2_scheme_account)) -> dict:
    try:
        payload = jwt.decode(token, secret, algorithms=[encrypt_algorithm])
    except (JWTError, AttributeError):
        raise HTTPException(status_code=401, detail="Неавторизованный аккаунт")
    return payload


def get_auth_account_id(payload: dict = Depends(get_payload_from_token)) -> int:
    try:
        id_: int = int(payload.get('sub'))  # type: ignore
    except ValueError:
        raise HTTPException(status_code=401, detail="Невалидный токен")
    return id_


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


def get_payload_from_token_optional(
        token: str = Depends(oauth2_scheme_account)) -> Optional[dict]:
    try:
        payload = jwt.decode(token, secret, algorithms=[encrypt_algorithm])
    except (JWTError, AttributeError):
        return None
    return payload


def get_auth_account_id_unverified(payload: dict = Depends(get_payload_from_token)) -> int:
    try:
        id_: int = int(payload.get('sub'))  # type: ignore
    except ValueError:
        raise HTTPException(status_code=401, detail="Неавторизованный аккаунт")
    return id_


class PagesPaginationParams:
    def __init__(
            self,
            limit: int = Query(50, ge=0, le=1_000),
            offset: int = Query(0, ge=0, alias='skip'),
    ) -> None:
        self.limit = limit
        self.offset = offset
