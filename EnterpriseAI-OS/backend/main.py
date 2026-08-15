#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - Main Application
نظام إدارة المؤسسات المتكامل بالذكاء الاصطناعي
"""

import asyncio
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.config import settings
from core.engine import EnterpriseEngine
from core.event_bus import EventBus
from core.security import SecurityManager
from core.audit import AuditLogger
from api.routes import router as api_router
from api.websocket import websocket_manager
from ai_engine.orchestrator import AIOrchestrator

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# === نماذج Pydantic ===
class AIQuery(BaseModel):
    query: str
    agent_type: str
    department: str
    context: Dict[str, Any] = {}


class TrainingData(BaseModel):
    training_data: list
    epochs: int = 10


# === دوال فحص الصحة ===
async def check_database() -> str:
    """فحص قاعدة البيانات"""
    try:
        # TODO: تنفيذ فحص فعلي
        return "healthy"
    except Exception:
        return "unhealthy"


async def check_redis() -> str:
    """فحص Redis"""
    try:
        # TODO: تنفيذ فحص فعلي
        return "healthy"
    except Exception:
        return "unhealthy"


async def check_ai_engine() -> str:
    """فحص محرك الذكاء الاصطناعي"""
    try:
        # TODO: تنفيذ فحص فعلي
        return "healthy"
    except Exception:
        return "unhealthy"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """إدارة دورة حياة التطبيق"""
    # بدء التشغيل
    logger.info("🚀 EnterpriseAI-OS يبدأ التشغيل...")

    # تهيئة المحرك
    app.state.engine = EnterpriseEngine()
    await app.state.engine.initialize()

    # تهيئة منسق الذكاء الاصطناعي
    app.state.ai_orchestrator = AIOrchestrator()
    await app.state.ai_orchestrator.initialize()

    # تهيئة ناقل الأحداث
    app.state.event_bus = EventBus()
    await app.state.event_bus.connect()

    logger.info("✅ EnterpriseAI-OS جاهز للعمل!")

    yield

    # الإغلاق
    logger.info("🛑 EnterpriseAI-OS يتم إيقافه...")
    await app.state.ai_orchestrator.shutdown()
    await app.state.event_bus.disconnect()
    await app.state.engine.shutdown()
    logger.info("✅ تم الإيقاف بنجاح")


# إنشاء التطبيق
app = FastAPI(
    title="EnterpriseAI-OS",
    description="نظام إدارة المؤسسات المتكامل بالذكاء الاصطناعي",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# === Middleware ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """إضافة ترويسات الأمان"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """تسجيل الطلبات"""
    start_time = asyncio.get_event_loop().time()
    response = await call_next(request)
    process_time = asyncio.get_event_loop().time() - start_time

    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )
    return response


# === Routes ===
app.include_router(api_router, prefix="/api/v1")


# === Health Check ===
@app.get("/health")
async def health_check():
    """فحص صحة النظام"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": await check_database(),
            "redis": await check_redis(),
            "ai_engine": await check_ai_engine(),
        }
    }


@app.get("/")
async def root():
    """الصفحة الرئيسية"""
    return {
        "name": "EnterpriseAI-OS",
        "version": "1.0.0",
        "description": "نظام إدارة المؤسسات المتكامل بالذكاء الاصطناعي",
        "docs": "/docs",
        "health": "/health"
    }


# === WebSocket ===
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """نقطة اتصال WebSocket للتحديثات الفورية"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await websocket_manager.handle_message(websocket, data)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket_manager.disconnect(websocket)


# === AI Endpoints ===
@app.post("/api/v1/ai/query")
async def ai_query(query: AIQuery):
    """استعلام الذكاء الاصطناعي"""
    from ai_engine.agents.base_agent import Task
    response = await app.state.ai_orchestrator.route_task(
        Task(
            id=f"query-{datetime.utcnow().timestamp()}",
            type=query.agent_type,
            data={"query": query.query, "context": query.context},
            user_id="anonymous",
            department=query.department
        )
    )
    return response


@app.get("/api/v1/ai/agents/status")
async def agents_status():
    """حالة الوكلاء"""
    return await app.state.ai_orchestrator.get_agents_status()


@app.post("/api/v1/ai/agents/{agent_id}/train")
async def train_agent(agent_id: str, training_data: TrainingData):
    """تدريب وكيل"""
    return await app.state.ai_orchestrator.train_agent(agent_id, training_data)


# === Error Handlers ===
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """معالج الأخطاء العام"""
    logger.error(f"Global error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "path": request.url.path
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=4 if not settings.DEBUG else 1
    )
