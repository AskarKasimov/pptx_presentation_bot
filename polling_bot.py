import logging
import sys
import asyncio

from os import getenv
from aiogram import Bot, Dispatcher, Router
from handlers import common

TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

dp = Dispatcher()

# Defining handlers
router = common.router

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
