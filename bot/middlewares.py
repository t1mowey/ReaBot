from typing import Callable, Dict, Any, Awaitable

import httpx
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class HttpxMiddleware(BaseMiddleware):
    def __init__(self, client: httpx.AsyncClient):
        super().__init__()
        self.client = client

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # прокидываем клиент в data
        data["client"] = self.client
        return await handler(event, data)