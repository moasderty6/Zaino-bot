# استخدام Python الرسمي
FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ الملفات
COPY . .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# تشغيل البوت
CMD ["python", "main.py"]
