import httpx
from fastapi import APIRouter, Request, Depends, BackgroundTasks, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.calendar.services import update_token, exchange_code_for_tokens
from app.exceptions import UserNotFoundError, RefreshTokenUpdateError
from app.conf import CLIENT_ID, get_db, REDIRECT_URI

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
SCOPE = "https://www.googleapis.com/auth/calendar"

router = APIRouter(tags=["Google Calendar"])


import random
from fastapi.responses import HTMLResponse

SUCCESS_MESSAGES = [
    "Вы молодец! Авторизация прошла успешно ✅",
    "Отлично! Мы всё сохранили 🔐",
    "Google Calendar подключён 🚀",
    "Красавчик! Всё работает 💯",
    "Done! Теперь можно вернуться в бота 😉",
]

@router.get("/oauth2callback")
async def oauth2callback(code: str, state: str, db: AsyncSession = Depends(get_db)):
    tokens = await exchange_code_for_tokens(code=code)
    refresh_token = tokens.get("refresh_token")
    user_id = int(state)

    await update_token(db, user_id, refresh_token)

    # случайная надпись
    msg = random.choice(SUCCESS_MESSAGES)

    html_content = f"""
        <html>
          <head>
            <meta charset="utf-8">
            <title>Авторизация завершена</title>
            <style>
              body {{
                font-family: Times New Roman, sans-serif;
                text-align: center;
                margin-top: 100px;
                background: #f9f9f9;
              }}
              h2 {{
                color: #333;
                margin-bottom: 40px;
              }}
              .btn {{
                display: inline-block;
                padding: 12px 24px;
                font-size: 16px;
                cursor: pointer;
                border-radius: 8px;
                border: none;
                background: #2AABEE; /* цвет Telegram */
                color: white;
                text-decoration: none;
                transition: background 0.3s ease;
              }}
              .btn:hover {{
                background: #229ED9;
              }}
            </style>
          </head>
          <body>
            <h2>{msg}</h2>
            <a href="https://t.me/dvfbgnhfd_bot" class="btn">🔙 Вернуться в Telegram</a>
          </body>
        </html>
        """
    return HTMLResponse(content=html_content)


@router.get("/calendar/register")
async def register_calendar(user_id: int):
    url = (
        f"{AUTH_URL}?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPE}"
        f"&access_type=offline"
        f"&prompt=consent"
        f"&state={user_id}"

    )
    return RedirectResponse(url)


# async def get_access_token(refresh_token: str) -> str | None:
#     """Обновляем access_token по refresh_token"""
#     async with httpx.AsyncClient() as client:
#         resp = await client.post(
#             TOKEN_URL,
#             data={
#                 "client_id": CLIENT_ID,
#                 "client_secret": CLIENT_SECRET,
#                 "refresh_token": refresh_token,
#                 "grant_type": "refresh_token",
#             },
#             headers={"Content-Type": "application/x-www-form-urlencoded"},
#         )
#
#     data = resp.json()
#     return data.get("access_token")
