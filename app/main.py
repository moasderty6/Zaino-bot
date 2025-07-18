import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties

# تحميل متغيرات البيئة
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# /start
@dp.message(F.text.startswith("/start"))
async def start_handler(message: types.Message):
    await message.answer(
        "🤖 أهلاً بك في بوت Zeno! البوت يعمل الآن.\n\nللتواصل: @Sasam132",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="📬 تواصل مع زينو", url="https://t.me/Sasam132")]
            ]
        )
    )

# رد افتراضي
@dp.message()
async def default_handler(message: types.Message):
    await message.answer("📩 أرسل /start للبدء!")

# Root للتأكيد فقط
async def handle_root(request):
    return web.Response(text="✅ Zeno Bot is Live!")

# Main
async def main():
    app = web.Application()
    app.router.add_get("/", handle_root)

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
