import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7924976888:AAGOQMEmMOhx8IJblL0oZ9rDafc6uVXQNNY"

app = Flask(__name__)

# إنشاء تطبيق التلجرام
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! يرجى العلم أن Vercel لا يدعم تحميل الملفات الكبيرة.\nسأقوم بمعالجة طلبك كـ Webhook.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ملاحظة: التحميل الفعلي لـ MP3 على Vercel شبه مستحيل للخطة المجانية
    # سنكتفي هنا بالرد للتأكد أن البوت شغال
    await update.message.reply_text(f"وصلني الرابط: {update.message.text}\nنصيحة: استخدم Koyeb أو Railway لتحميل الـ MP3 فعلياً.")

@app.route('/api/index', methods=['POST'])
def webhook():
    if request.method == "POST":
        asyncio.run(application.initialize())
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.process_update(update))
        return "ok", 200

@app.route('/')
def index():
    return "Bot is Alive!"
