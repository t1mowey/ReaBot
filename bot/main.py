import asyncio

from app.conf import WEBHOOK_URL
from bot_instance import bot, dp


async def run_polling():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        print("drop pending error: ", str(e))
    # try:
    #     await bot.send_message(MY_ID, "✅ Бот запущен локально (polling)")
    # except Exception as e:
    #     print("start message error: ", str(e))

    await dp.start_polling(bot)


# async def restore_webhook():
#     try:
#         await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=False)
#         await bot.send_message(MY_ID, f"🔄 Bot set on VPS")
#     except Exception as e:
#         print("restore webhook error:", str(e))
#     finally:
#         await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(run_polling())
    except KeyboardInterrupt:
        print("Bot stopped by user")
        # asyncio.run(restore_webhook())