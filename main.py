from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
import asyncio
import logging
import os

# التوكن من متغير البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")

# إعداد البوت والديسباتشر
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# إنشاء الأزرار
def start_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📢 قناة زينو ياسر محاميد الرسمية",
            url="https://t.me/zainaldinmaham1"
        )],
        [InlineKeyboardButton(
            text="🗣 منتدى شبكة زينو الإخبارية",
            url="https://t.me/+qaY85ZwO0HQwOGY0"
        )]
    ])
    return keyboard


# أمر /start
@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        text="أهلاً بك 👋\nاختر من الأزرار أدناه للانضمام:",
        reply_markup=start_keyboard(),
        parse_mode=ParseMode.HTML
    )


# تشغيل البوت
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
