#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - Shared Models
النماذج المشتركة
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List


class CommandStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class DomainEvent:
    """حدث النطاق"""
    id: str
    aggregate_id: str
    aggregate_type: str
    event_type: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: int = 1
    created_at: datetime = field(default_factory=datetime.utcnow)

    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "event_type": self.event_type,
            "payload": self.payload,
            "metadata": self.metadata,
            "version": self.version,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class Command:
    """الأمر"""
    id: str
    type: str
    data: Dict[str, Any]
    user_id: str
    department: str
    status: CommandStatus = CommandStatus.PENDING
    result: Any = None
    events: List[DomainEvent] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    async def execute(self) -> 'Command':
        """تنفيذ الأمر - يتم تجاوزه في الفئات الفرعية"""
        raise NotImplementedError
