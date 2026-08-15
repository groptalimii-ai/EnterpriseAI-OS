#!/bin/bash
# EnterpriseAI-OS Setup Script
# سكربت الإعداد الأولي

set -e

echo "🚀 EnterpriseAI-OS - سكربت الإعداد"
echo "===================================="

# التحقق من المتطلبات
echo "📋 التحقق من المتطلبات..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker غير مثبت. يرجى تثبيت Docker أولاً."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose غير مثبت. يرجى تثبيته أولاً."
    exit 1
fi

echo "✅ Docker و Docker Compose موجودان"

# إنشاء ملف .env
if [ ! -f config/.env ]; then
    echo "📝 إنشاء ملف الإعدادات..."
    cp config/.env.example config/.env
    echo "⚠️ يرجى تعديل config/.env بإعداداتك قبل التشغيل"
fi

# إنشاء المجلدات
mkdir -p data models logs

# بناء الصور
echo "🔨 بناء صور Docker..."
docker-compose -f docker-compose.full.yml build

# تهيئة قاعدة البيانات
echo "🗄️ تهيئة قاعدة البيانات..."
docker-compose -f docker-compose.full.yml up -d postgres redis
echo "⏳ انتظار قاعدة البيانات..."
sleep 10

# تشغيل الترحيلات
echo "🔄 تشغيل ترحيلات قاعدة البيانات..."
docker-compose -f docker-compose.full.yml run --rm backend alembic upgrade head

# إنشاء المستخدم الأول
echo "👤 إنشاء المستخدم الأول..."
python backend/scripts/create_superuser.py

# تشغيل النظام
echo "🚀 تشغيل EnterpriseAI-OS..."
docker-compose -f docker-compose.full.yml up -d

echo ""
echo "✅ تم الإعداد بنجاح!"
echo ""
echo "📍 الوصول إلى النظام:"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Grafana:  http://localhost:3001"
echo ""
echo "📖 للمزيد من المعلومات، راجع docs/DEPLOYMENT.md"
