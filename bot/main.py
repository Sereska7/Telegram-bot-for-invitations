import asyncio
import redis

from aiogram import Bot, Dispatcher

from bot.core.config import settings
from bot.handlers.commands import router as router_comm
from bot.handlers.hendlers_register_profile import router as router_register
from bot.handlers.handlers_main_manu import router as router_menu


redis_client = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_HOST, db=settings.REDIS_DB
)


async def main():
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()
    dp.include_router(router_comm)
    dp.include_router(router_register)
    dp.include_router(router_menu)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Bot online")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot offline")
