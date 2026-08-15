#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - Core Engine
المحرك الأساسي للنظام
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any

from core.config import settings
from core.models import Command, DomainEvent, CommandStatus
from core.event_bus import EventBus
from core.security import SecurityManager
from core.audit import AuditLogger

logger = logging.getLogger(__name__)


class ConcreteCommand(Command):
    """أمر قابل للتنفيذ"""

    async def execute(self) -> "Command":
        """تنفيذ الأمر - يتم تجاوزه في الفئات الفرعية"""
        logger.info(f"تنفيذ الأمر: {self.type}")
        # تنفيذ افتراضي - يمكن تجاوزه
        return self


class EnterpriseEngine:
    """المحرك الأساسي للنظام"""

    def __init__(self):
        self.event_bus: Optional[EventBus] = None
        self.security_manager: Optional[SecurityManager] = None
        self.audit_logger: Optional[AuditLogger] = None
        self.command_handlers: Dict[str, Any] = {}
        self.event_handlers: Dict[str, List[Any]] = {}
        self.initialized = False

    async def initialize(self):
        """تهيئة المحرك"""
        if self.initialized:
            return

        logger.info("🔧 تهيئة المحرك الأساسي...")

        # تهيئة المكونات
        self.event_bus = EventBus()
        await self.event_bus.connect()

        self.security_manager = SecurityManager()
        await self.security_manager.initialize()

        self.audit_logger = AuditLogger()
        await self.audit_logger.initialize()

        # تسجيل معالجات الأحداث الافتراضية
        self._register_default_handlers()

        self.initialized = True
        logger.info("✅ تم تهيئة المحرك بنجاح")

    def _register_default_handlers(self):
        """تسجيل معالجات الأحداث الافتراضية"""
        self.event_handlers["user.created"] = [self._on_user_created]
        self.event_handlers["transaction.completed"] = [self._on_transaction_completed]
        self.event_handlers["inventory.updated"] = [self._on_inventory_updated]
        self.event_handlers["purchase_order.created"] = [self._on_purchase_order_created]

    async def process_command(self, command: Command) -> Command:
        """معالجة أمر"""
        logger.info(f"📋 معالجة الأمر: {command.type} ({command.id})")

        try:
            # 1. التحقق من الصلاحيات
            await self.security_manager.authorize(command)

            # 2. تسجيل بداية المعالجة
            command.status = CommandStatus.PROCESSING
            await self.audit_logger.log_command_start(command)

            # 3. تنفيذ الأمر
            # إذا كان الأمر من ConcreteCommand أو فئة فرعية
            if hasattr(command, "execute") and callable(command.execute):
                result = await command.execute()
            else:
                result = {"status": "no_executor", "message": "No execute method available"}

            # 4. تحديث الحالة
            command.status = CommandStatus.COMPLETED
            command.result = result

            # 5. نشر الأحداث
            for event in command.events:
                await self.event_bus.publish(event)
                await self._dispatch_event(event)

            # 6. تسجيل الإكمال
            await self.audit_logger.log_command_complete(command)

            logger.info(f"✅ تم إكمال الأمر: {command.type} ({command.id})")

        except Exception as e:
            command.status = CommandStatus.FAILED
            command.result = {"error": str(e)}
            await self.audit_logger.log_command_failed(command, e)
            logger.error(f"❌ فشل الأمر: {command.type} ({command.id}) - {e}")
            raise

        return command

    async def _dispatch_event(self, event: DomainEvent):
        """إرسال الحدث للمعالجات"""
        handlers = self.event_handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(f"Error in event handler: {e}")

    async def _on_user_created(self, event: DomainEvent):
        logger.info(f"👤 مستخدم جديد: {event.payload.get('email')}")

    async def _on_transaction_completed(self, event: DomainEvent):
        logger.info(f"💰 معاملة مكتملة: {event.payload.get('amount')}")

    async def _on_inventory_updated(self, event: DomainEvent):
        logger.info(f"📦 تحديث مخزون: {event.payload.get('item_id')}")

    async def _on_purchase_order_created(self, event: DomainEvent):
        logger.info(f"🛒 طلب شراء جديد: {event.payload.get('order_id')}")

    async def shutdown(self):
        """إيقاف المحرك"""
        logger.info("🔧 إيقاف المحرك...")
        if self.event_bus:
            await self.event_bus.disconnect()
        if self.security_manager:
            await self.security_manager.shutdown()
        if self.audit_logger:
            await self.audit_logger.shutdown()
        logger.info("✅ تم إيقاف المحرك")