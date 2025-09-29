from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from httpx import AsyncClient

from bot.conf import CALENDAR_LINK, BASE_URL


class Registration(StatesGroup):
    get_refresh = State()
    set_group = State()


kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Готово", callback_data="get_refresh")]])

router = Router()


@router.message(F.text == "/register")
async def register(msg: Message, client: AsyncClient):
    # url = "https://localhost:8000/calendar/register"
    resp = await client.get(f"{BASE_URL}/users/get", params={"t_id": msg.from_user.id})
    res = resp.json()
    url = f'{BASE_URL}/calendar/register?user_id={res.get("id")}'
    await msg.answer(text=f'Авторизуйтесь по ссылке: <a href="{url}">перейти</a>\n'
                     f'Ссылка: {url}', parse_mode="HTML", reply_markup=kb)