from aiogram.types import Update
from fastapi import FastAPI, Request, BackgroundTasks

from app.conf import setup_logger, logger
from app.calendar import google_calendar
from app.registration import registration

setup_logger()

app = FastAPI()
app.include_router(google_calendar.router)
app.include_router(registration.router)


# @app.lifespan("startup")
# async def setup_webhook():
#     logger.info("New version of bot deployed and started")


# @app.post("/tg")
# async def tg_webhook(request: Request, bt: BackgroundTasks):
#     update = Update.model_validate(await request.json())
#     bt.add_task(dp.feed_update, bot, update)
#     return {"ok": True}