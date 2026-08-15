FROM python:3.11-slim

WORKDIR /app

# تثبيت التبعيات النظامية
RUN apt-get update && apt-get install -y     gcc     g++     libpq-dev     libssl-dev     libffi-dev     git     && rm -rf /var/lib/apt/lists/*

# نسخ ملفات التبعيات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# إنشاء المجلدات المطلوبة
RUN mkdir -p /data /models /logs

# المستخدم غير الجذر
RUN useradd -m -u 1000 enterpriseai && chown -R enterpriseai:enterpriseai /app
USER enterpriseai

# المنفذ
EXPOSE 8000

# الأمر الافتراضي
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
