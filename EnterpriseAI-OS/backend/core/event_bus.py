#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - Event Bus
ناقل الأحداث
"""

import asyncio
import json
import logging
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from core.config import settings
from core.models import DomainEvent

logger = logging.getLogger(__name__)


class EventBus:
    """ناقل أحداث Kafka-based"""

    def __init__(self):
        self.producer: Optional[AIOKafkaProducer] = None
        self.consumers: Dict[str, AIOKafkaConsumer] = {}
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_store: List[Dict] = []
        self.connected = False

    async def connect(self):
        """الاتصال بـ Kafka"""
        if self.connected:
            return

        logger.info("🔗 الاتصال بـ Kafka...")

        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None
        )
        await self.producer.start()

        self.connected = True
        logger.info("✅ تم الاتصال بـ Kafka")

    async def disconnect(self):
        """قطع الاتصال"""
        if self.producer:
            await self.producer.stop()
        for consumer in self.consumers.values():
            await consumer.stop()
        self.connected = False
        logger.info("🔌 تم قطع الاتصال بـ Kafka")

    async def publish(self, event: DomainEvent, topic: Optional[str] = None):
        """نشر حدث"""
        if not self.connected:
            raise RuntimeError("EventBus not connected")

        topic = topic or f"{settings.KAFKA_TOPIC_PREFIX}.{event.aggregate_type}"

        # تخزين في Event Store
        event_data = event.serialize()
        self.event_store.append(event_data)

        # نشر لـ Kafka
        await self.producer.send(
            topic=topic,
            value=event_data,
            key=event_data.get("aggregate_id")
        )

        logger.debug(f"📤 حدث منشور: {topic} - {event_data.get('event_type')}")

    async def subscribe(self, topic: str, handler: Callable):
        """الاشتراك في موضوع"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []

            # إنشاء مستهلك جديد
            consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                group_id=f"enterpriseai-{topic}",
                auto_offset_reset="latest"
            )
            await consumer.start()
            self.consumers[topic] = consumer

            # بدء مهمة الاستماع
            asyncio.create_task(self._consume(topic, consumer))

        self.subscribers[topic].append(handler)
        logger.info(f"👂 اشتراك جديد: {topic}")

    async def _consume(self, topic: str, consumer: AIOKafkaConsumer):
        """استهلاك الرسائل"""
        try:
            async for message in consumer:
                event_data = message.value
                handlers = self.subscribers.get(topic, [])
                for handler in handlers:
                    try:
                        await handler(event_data)
                    except Exception as e:
                        logger.error(f"Error in handler for {topic}: {e}")
        except Exception as e:
            logger.error(f"Consumer error for {topic}: {e}")

    async def get_events(self, aggregate_id: str, limit: int = 100) -> List[Dict]:
        """الحصول على أحداث لمجموع معين"""
        events = [
            e for e in self.event_store
            if e.get("aggregate_id") == aggregate_id
        ]
        return events[-limit:]