import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start(message: Message):
    kb = [
        [
            {"text": "📢 قناة زينو ياسر محاميد الرسمية", "url": "https://t.me/zainaldinmaham1"},
        ],
        [
            {"text": "🗣 منتدى شبكة زينو الإخبارية", "url": "https://t.me/+qaY85ZwO0HQwOGY0"},
        ],
        [
            {"text": "📬 للتواصل مع زينو", "url": "https://t.me/Sasam132"},
        ]
    ]
    inline_kb = [[InlineKeyboardButton(**btn) for btn in row] for row in kb]
    await message.answer("أهلاً بك في بوت زينو 👋", reply_markup=InlineKeyboardMarkup(inline_kb))

# ✅ استبدال WebhookRequestHandler بهذه الدالة
async def handle_webhook(request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

async def on_startup(app):
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

async def main():
    app = web.Application()
    app.router.add_post("/webhook", handle_webhook)  # ✅ تعديل هنا
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"Running on port {PORT}...")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
