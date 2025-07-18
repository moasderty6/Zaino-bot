import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv

from handlers import router  # تأكد أن الملف اسمه handlers.py

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)  # تسجيل الهاندلرات

# صفحة جذر لإثبات أن السيرفر شغال
async def handle_root(request):
    return web.Response(text="✅ Zeno Bot is Live!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_post("/webhook", SimpleRequestHandler(dispatcher=dp, bot=bot))
    setup_application(app, dp, bot=bot)

    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    print(f"✅ Running on http://0.0.0.0:{PORT}")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
