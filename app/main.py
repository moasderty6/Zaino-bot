import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update

# بيئة التشغيل
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL").rstrip("/")  # إزالة / زائدة
PORT = int(os.environ.get("PORT", 8080))

# إنشاء البوت والموزع
bot = Bot(token=TOKEN)
dp = Dispatcher()

# أوامر البوت
@dp.message(F.command("start"))
async def start(message: Message):
    kb = [
        [
            {"text": "📢 قناة زينو ياسر محاميد الرسمية", "url": "https://t.me/Tgstarssavebot"},
        ],
        [
            {"text": "🗣 منتدى شبكة زينو الإخبارية", "url": "https://t.me/Tgstarssavebot"},
        ],
        [
            {"text": "📬 للتواصل مع زينو", "url": "https://t.me/Tgstarssavebot"},
        ]
    ]
    inline_kb = [[InlineKeyboardButton(**btn) for btn in row] for row in kb]
    await message.answer("أهلاً بك في بوت زينو 👋", reply_markup=InlineKeyboardMarkup(inline_kb))

# استقبال التحديثات من تيليغرام
async def handle_webhook(request):
    try:
        data = await request.json()
        print("✅ Webhook received:", data)  # فحص الرسالة
        update = Update(**data)  # أكثر مرونة من model_validate
        await dp.feed_update(bot, update)
        return web.Response(text="OK")
    except Exception as e:
        print("❌ Webhook error:", e)
        return web.Response(status=500, text="Internal Server Error")

# صفحة فحص للرابط الأساسي /
async def homepage(request):
    return web.Response(text="بوت زينو يعمل ✅")

# عند بدء التشغيل
async def on_startup(app):
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    print(f"✅ Webhook set: {WEBHOOK_URL}/webhook")

# عند الإغلاق
async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

# تشغيل السيرفر
async def main():
    app = web.Application()
    app.router.add_get("/", homepage)
    app.router.add_post("/webhook", handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"🚀 Bot running on port {PORT}...")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
