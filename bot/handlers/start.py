from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from httpx import AsyncClient

from bot.conf import BASE_URL


router = Router()


@router.message(Command("start"))
async def start(msg: Message,
                client: AsyncClient):
    resp = await client.post(
    f"{BASE_URL}/users/register",
    params={"user_id": msg.from_user.id}
)
    print(resp)
    # await register_user(msg.from_user)
    await msg.answer("Привет! Это бот для дублирования расписания в сторонний календарь\n"
                     f"Напиши /register, чтобы добавить своё расписание")