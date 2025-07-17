import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# ========================
# إعدادات البوت
# ========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing!")

WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")  # مثل: https://zino-bot.onrender.com
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# ========================
# إنشاء كائنات البوت
# ========================
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ========================
# أزرار التوجيه
# ========================
def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📢 قناة زينو ياسر محاميد الرسمية",
            url="https://t.me/zainaldinmaham1"
        )],
        [InlineKeyboardButton(
            text="🗣 منتدى شبكة زينو الإخبارية",
            url="https://t.me/+qaY85ZwO0HQwOGY0"
        )]
    ])


# ========================
# أمر /start
# ========================
@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "أهلاً بك 👋\nاختر من الأزرار أدناه للانضمام:",
        reply_markup=start_keyboard(),
        parse_mode=ParseMode.HTML
    )


# ========================
# إعداد Webhook عند بدء التشغيل
# ========================
@dp.startup()
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to: {WEBHOOK_URL}")


# ========================
# تشغيل تطبيق Aiohttp
# ========================
async def main():
    app = web.Application()
    app["bot"] = bot

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp)

    port = int(os.getenv("PORT", "8080"))
    web.run_app(app, port=port)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
