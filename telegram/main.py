import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from tasks.schedulers import scheduler
from handlers.start import start_message
from config import TOKEN

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

dp.include_router(start_message)

async def main() -> None:
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
