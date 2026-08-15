# 🚀 EnterpriseAI-OS Deployment Guide

## دليل النشر الكامل

---

## 📋 المتطلبات المسبقة

### البرمجيات المطلوبة
- Docker 24.0+
- Docker Compose 2.20+
- Git 2.40+
- (اختياري) Kubernetes 1.28+
- (اختياري) NVIDIA Docker Runtime (للـ GPU)

### الموارد المطلوبة

#### النشر الصغير (حتى 50 مستخدم)
```yaml
CPU: 8 cores
RAM: 32 GB
Storage: 500 GB SSD
Network: 1 Gbps
```

#### النشر المتوسط (50-500 مستخدم)
```yaml
CPU: 16 cores
RAM: 64 GB
Storage: 1 TB NVMe SSD
Network: 10 Gbps
GPU: NVIDIA RTX 4090 (8GB VRAM)
```

#### النشر الكبير (500+ مستخدم)
```yaml
CPU: 32+ cores
RAM: 128+ GB
Storage: 2 TB NVMe SSD RAID
Network: 10 Gbps+
GPU: NVIDIA A100 (40GB VRAM)
```

---

## 🐳 النشر باستخدام Docker Compose

### الخطوة 1: استنساخ المستودع
```bash
git clone https://github.com/your-org/EnterpriseAI-OS.git
cd EnterpriseAI-OS
```

### الخطوة 2: إعداد ملف البيئة
```bash
cp config/.env.example config/.env
nano config/.env  # أو أي محرر
```

### الخطوة 3: إنشاء الشبكة
```bash
docker network create enterpriseai-network
```

### الخطوة 4: التشغيل
```bash
# النشر الكامل
docker-compose -f docker-compose.full.yml up -d

# أو النشر الأدنى
docker-compose -f docker-compose.minimal.yml up -d

# أو النشر المخصص
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### الخطوة 5: التحقق
```bash
# حالة الخدمات
docker-compose ps

# سجلات
docker-compose logs -f backend
docker-compose logs -f frontend

# صحة النظام
curl http://localhost:8000/health
curl http://localhost:3000/health
```

---

## ☸️ النشر باستخدام Kubernetes

### الخطوة 1: إعداد المجموعة
```bash
# إنشاء namespace
kubectl create namespace enterpriseai

# إعداد secrets
kubectl create secret generic db-credentials   --from-literal=password=your-secure-password   -n enterpriseai

# إعداد configmap
kubectl apply -f kubernetes/configmap.yaml
```

### الخطوة 2: نشر قواعد البيانات
```bash
kubectl apply -f kubernetes/databases/postgresql.yaml
kubectl apply -f kubernetes/databases/redis.yaml
kubectl apply -f kubernetes/databases/clickhouse.yaml
kubectl apply -f kubernetes/databases/milvus.yaml
```

### الخطوة 3: نشر الوكلاء
```bash
kubectl apply -f kubernetes/agents/financial-agent.yaml
kubectl apply -f kubernetes/agents/inventory-agent.yaml
kubectl apply -f kubernetes/agents/production-agent.yaml
# ... إلخ
```

### الخطوة 4: نشر الواجهات
```bash
kubectl apply -f kubernetes/backend.yaml
kubectl apply -f kubernetes/frontend.yaml
kubectl apply -f kubernetes/ingress.yaml
```

### الخطوة 5: التحقق
```bash
kubectl get pods -n enterpriseai
kubectl get svc -n enterpriseai
kubectl get ingress -n enterpriseai
```

---

## 🔧 التكوين

### ملف .env الرئيسي
```env
# === البيئة ===
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-super-secret-key-here

# === قاعدة البيانات ===
DATABASE_URL=postgresql://user:pass@postgres:5432/enterpriseai
CLICKHOUSE_URL=clickhouse://clickhouse:8123/enterpriseai
REDIS_URL=redis://redis:6379/0

# === الذكاء الاصطناعي ===
AI_MODEL_PATH=/models
AI_GPU_ENABLED=true
AI_BATCH_SIZE=32
AI_MAX_TOKENS=4096

# === الأمان ===
JWT_SECRET=your-jwt-secret
JWT_EXPIRY=24h
ENCRYPTION_KEY=your-encryption-key
MFA_ENABLED=true

# === التكامل ===
SMTP_HOST=smtp.company.com
SMTP_PORT=587
SMTP_USER=noreply@company.com
SMTP_PASS=your-smtp-password

# === المراقبة ===
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
SENTRY_DSN=your-sentry-dsn
```

---

## 🔄 التحديث

### تحديث Docker
```bash
# سحب آخر التحديثات
git pull origin main

# إعادة البناء
docker-compose -f docker-compose.full.yml build --no-cache

# التحديث بدون توقف
docker-compose -f docker-compose.full.yml up -d --no-deps --build backend
docker-compose -f docker-compose.full.yml up -d --no-deps --build frontend
```

### تحديث Kubernetes
```bash
# تحديث الصورة
kubectl set image deployment/backend   backend=enterpriseai/backend:v2.0.0   -n enterpriseai

# التحقق من التحديث
kubectl rollout status deployment/backend -n enterpriseai
```

---

## 📊 المراقبة

### Grafana Dashboards
- http://localhost:3001 (افتراضي)
- الـ Dashboards متضمنة:
  - System Health
  - AI Performance
  - Business KPIs
  - Security Events

### Prometheus Metrics
- http://localhost:9090
- Metrics متضمنة:
  - request_duration_seconds
  - ai_prediction_accuracy
  - database_connections
  - active_users

### Logs
```bash
# عبر Docker
docker-compose logs -f --tail=100

# عبر Kubernetes
kubectl logs -f deployment/backend -n enterpriseai --all-containers

# عبر Loki (إذا مُفعّل)
curl -G "http://localhost:3100/loki/api/v1/query"   --data-urlencode 'query={app="backend"}'
```

---

## 🆘 استكشاف الأخطاء

### المشكلة: النظام بطيء
```bash
# التحقق من الموارد
docker stats

# التحقق من قاعدة البيانات
docker-compose exec postgres psql -U user -d enterpriseai -c "SELECT * FROM pg_stat_activity;"

# التحقق من Redis
docker-compose exec redis redis-cli INFO
```

### المشكلة: الوكلاء لا يستجيبون
```bash
# إعادة تشغيل الوكلاء
docker-compose restart financial-agent inventory-agent

# التحقق من سجلات الوكلاء
docker-compose logs financial-agent | tail -n 50
```

### المشكلة: قاعدة البيانات
```bash
# إصلاح PostgreSQL
docker-compose exec postgres pg_dump -U user enterpriseai > backup.sql
docker-compose exec postgres psql -U user -d enterpriseai -c "REINDEX DATABASE enterpriseai;"
```

---

## 📞 الدعم

إذا واجهت مشاكل:
1. تحقق من [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. افتح Issue على GitHub
3. تواصل معنا: support@enterpriseai-os.com
