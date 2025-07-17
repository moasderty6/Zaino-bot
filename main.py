import os
import asyncio
import logging
import threading

from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ========================
# إعدادات البوت
# ========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
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
        text="أهلاً بك 👋\nاختر من الأزرار أدناه للانضمام:",
        reply_markup=start_keyboard(),
        parse_mode=ParseMode.HTML
    )

# ========================
# سيرفر aiohttp (لبقاء البوت حيًا)
# ========================
async def handle(request):
    return web.Response(text="Bot is alive")

def run_web():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    web.run_app(app, port=8080)

# ========================
# تشغيل البوت
# ========================
async def main():
    # تشغيل السيرفر الصغير في خيط منفصل
    threading.Thread(target=run_web, daemon=True).start()

    # بدء البوت
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
