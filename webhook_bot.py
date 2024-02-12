import logging
import sys
from os import getenv

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers import common

TOKEN = getenv("BOT_TOKEN")
print(TOKEN)

WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 4444

WEBHOOK_PATH = "/pptx_tg"
WEBHOOK_SECRET = "secret1337bitchmf2"

BASE_WEBHOOK_URL = "https://server.askar.su"

# Defining handlers
router = common.router


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)


def main() -> None:
    dp = Dispatcher()
    # Including handlers
    dp.include_router(router)

    dp.startup.register(on_startup)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    # Create aiohttp.web.Application instance
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
