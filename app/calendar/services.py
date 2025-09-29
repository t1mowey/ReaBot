from http.client import HTTPException

import httpx
from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.conf import get_db, TOKEN_URL, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from app.exceptions import UserNotFoundError, RefreshTokenUpdateError
from app.repositories import get_user_by_t_id, update_google_token, get_user_by_id


async def exchange_code_for_tokens(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            TOKEN_URL,
            data={
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    resp.raise_for_status()
    return resp.json()


async def update_token(db: AsyncSession, user_id: int, refresh_token: str):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError(f"Not found user with t_id {user_id}")
    user_refresh = await update_google_token(db, user_id, refresh_token)
    if not user_refresh:
        raise RefreshTokenUpdateError(f"Error while updating token")
    return user_refresh




