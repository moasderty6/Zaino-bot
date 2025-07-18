import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

# إعدادات البوت
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# أوامر البوت الأساسية
@dp.message(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("🤖 أهلاً بك في بوت Zeno! البوت يعمل الآن بنجاح.")

# رَد افتراضي
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer("📩 أرسل /start للبدء!")

# نقطة البداية
async def main():
    # إعداد Web App
    app = web.Application()

    # مسار "/" الأساسي لعرض حالة السيرفر
    async def handle_root(request):
        return web.Response(text="✅ Zeno Bot is Live on Render!")

    app.router.add_get("/", handle_root)

    # إعداد webhook
    app.router.add_post("/webhook", SimpleRequestHandler(dispatcher=dp, bot=bot))

    # إعداد التطبيق
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    setup_application(app, dp, bot=bot)

    # تشغيل التطبيق
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"✅ Bot is running on port {PORT}")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
