import httpx
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from bot.conf import TOKEN
from bot.handlers import start
from bot.middlewares import HttpxMiddleware
# from services.middlewares import SessionMiddleware
# from handlers import start, client_panel, worker_panel
from handlers import register

bot = Bot(TOKEN)
dp = Dispatcher()

client = httpx.AsyncClient()

dp.update.middleware(HttpxMiddleware(client))

# dp.update.outer_middleware(SessionMiddleware())

dp.include_router(register.router)
dp.include_router(start.router)


