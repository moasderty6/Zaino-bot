import os
import asyncio
from aiohttp import web
from dotenv import load_dotenv
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot import bot, dp
from handlers import router

load_dotenv()

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

dp.include_router(router)

async def on_startup(bot):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(bot):
    await bot.delete_webhook()

async def main():
    app = web.Application()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    return app

if __name__ == "__main__":
    web.run_app(app=asyncio.run(main()), port=PORT)
