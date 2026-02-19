import asyncio
import os
import asyncpg  # تأكد من تثبيتها عبر pip install asyncpg
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, Update

# بيئة التشغيل
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL").rstrip("/")
PORT = int(os.environ.get("PORT", 8080))
DATABASE_URL = "postgresql://neondb_owner:npg_yPL6dYWRZQ4o@ep-little-firefly-aifch2tu-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

# إنشاء البوت والموزع
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- دالة للاتصال بقاعدة البيانات وإنشاء الجدول ---
async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    # إنشاء جدول المستخدمين إذا لم يكن موجوداً
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    return conn

# --- أوامر البوت ---

@dp.message(F.command("start"))
async def start(message: Message):
    # حفظ المستخدم في قاعدة البيانات
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute('''
            INSERT INTO users (user_id, username) 
            VALUES ($1, $2) 
            ON CONFLICT (user_id) DO NOTHING
        ''', message.from_user.id, message.from_user.username)
        await conn.close()
    except Exception as e:
        print(f"❌ DB Error: {e}")

    kb = [
        [{"text": "📢 قناة زينو ياسر محاميد الرسمية", "url": "https://t.me/zainaldinmaham1"}],
        [{"text": "🗣 منتدى شبكة زينو الإخبارية", "url": "https://t.me/zedan432"}],
        [{"text": "📬 للتواصل مع زينو", "url": "https://t.me/Sasam132"}]
    ]
    inline_kb = [[InlineKeyboardButton(**btn) for btn in row] for row in kb]
    await message.answer(f"أهلاً بك {message.from_user.first_name} في بوت زينو 👋\nتم تسجيلك في قاعدة البيانات بنجاح!", 
                         reply_markup=InlineKeyboardMarkup(inline_kb))

@dp.message(F.command("stats"))
async def get_stats(message: Message):
    # أمر لمشاهدة عدد المستخدمين
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        count = await conn.fetchval('SELECT COUNT(*) FROM users')
        await conn.close()
        await message.answer(f"📊 إحصائيات البوت:\n\nعدد المستخدمين المسجلين: **{count}**")
    except Exception as e:
        await message.answer("حدث خطأ أثناء جلب البيانات.")
        print(e)

# --- إدارة الويب هوك ---

async def handle_webhook(request):
    try:
        data = await request.json()
        update = Update(**data)
        await dp.feed_update(bot, update)
        return web.Response(text="OK")
    except Exception as e:
        return web.Response(status=500, text="Internal Server Error")

async def homepage(request):
    return web.Response(text="بوت زينو يعمل ✅")

async def on_startup(app):
    # إنشاء الجدول عند التشغيل
    await init_db()
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    print(f"✅ Database Ready & Webhook set")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

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
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
