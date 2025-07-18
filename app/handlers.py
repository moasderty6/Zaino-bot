from aiogram import Router, types, F

router = Router()

@router.message(F.text.startswith("/start"))
async def start_handler(message: types.Message):
    await message.answer(
        "🤖 أهلاً بك في بوت Zeno! البوت يعمل الآن.\n\nللتواصل: @Sasam132",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="📬 تواصل مع زينو", url="https://t.me/Sasam132")]
            ]
        )
    )

@router.message()
async def fallback_handler(message: types.Message):
    await message.answer("📩 أرسل /start للبدء!")
