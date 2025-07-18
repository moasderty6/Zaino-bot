import asyncio
from aiogram import types
from aiohttp import web
from bot import bot, dp
from handlers import router
import os

dp.include_router(router)

async def on_startup(app: web.Application):
    print("🔗 Bot started via webhook...")

async def on_shutdown(app: web.Application):
    await bot.session.close()

async def handle_request(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response()

async def main():
    app = web.Application()
    app.router.add_post(f"/webhook", handle_request)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Webhook setup
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")

    # Start server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()
    print(f"✅ Server running on port {os.getenv('PORT', 8080)}")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
