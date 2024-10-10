# استخدام صورة Python 3.8
FROM python:3.8-slim-buster

# تثبيت FFmpeg (الذي يحتوي على ffprobe)
RUN apt-get update && apt-get install -y ffmpeg

# تعيين مسار العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كل الملفات إلى الحاوية
COPY . .

# تشغيل التطبيق (مثل البوت)
CMD ["python", "bot.py"]
