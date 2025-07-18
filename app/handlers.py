from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 قناة زينو الرسمية", url="https://t.me/zainaldinmaham1")],
            [InlineKeyboardButton(text="🌐 منتدى شبكة زينو", url="https://t.me/+qaY85ZwO0HQwOGY0")],
            [InlineKeyboardButton(text="✉️ تواصل مع زينو", url="https://t.me/Sasam132")]
        ]
    )
    await message.answer(
        f"أهلًا وسهلًا فيك <b>{message.from_user.first_name}</b> 👋\n"
        "اختر من الأزرار التالية للتفاعل معنا:",
        reply_markup=keyboard
    )
