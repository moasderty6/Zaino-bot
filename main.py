import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# ========================
# الإعدادات
# ========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")  # مثل https://your-bot.onrender.com

if not BOT_TOKEN or not WEBHOOK_HOST:
    raise RuntimeError("❌ تأكد من وجود المتغيرات BOT_TOKEN و WEBHOOK_HOST في إعدادات السيرفر.")

WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ========================
# لوحة الأزرار
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
# إعداد Webhook تلقائيًا عند بدء التشغيل
# ========================
@dp.startup()
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"✅ Webhook تم تفعيله: {WEBHOOK_URL}")


# ========================
# خادم aiohttp لاستقبال التحديثات
# ========================
async def main():
    app = web.Application()
    app["bot"] = bot

    # تفعيل webhook handler
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp)

    # تشغيل على بورت 8080
    port = int(os.getenv("PORT", "8080"))
    logging.info(f"🚀 بدء السيرفر على البورت {port}")
    web.run_app(app, port=port)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
