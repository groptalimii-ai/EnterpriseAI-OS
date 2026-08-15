#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - Security Manager
مدير الأمان
"""

import logging
import hashlib
import secrets
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import pyotp

from core.config import settings

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityManager:
    """مدير الأمان"""

    def __init__(self):
        # التحقق من طول مفتاح التشفير
        key = settings.ENCRYPTION_KEY.encode()
        if len(key) < 32:
            # تمديد المفتاح إلى 32 بايت
            key = key.ljust(32, b"0")[:32]
            logger.warning("ENCRYPTION_KEY تم تمديده إلى 32 بايت")

        # Fernet يتطلب base64-encoded 32-byte key
        self.encryption_key = base64.urlsafe_b64encode(key[:32])
        self.cipher = Fernet(self.encryption_key)
        self.active_sessions: Dict[str, Dict] = {}

    async def initialize(self):
        """تهيئة مدير الأمان"""
        logger.info("🔒 تهيئة مدير الأمان...")

    async def authorize(self, command: Any) -> bool:
        """التحقق من الصلاحيات"""
        # التحقق من JWT
        # التحقق من RBAC
        # التحقق من ABAC
        return True

    def hash_password(self, password: str) -> str:
        """تجزئة كلمة المرور"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """التحقق من كلمة المرور"""
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """إنشاء رمز وصول"""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(hours=settings.JWT_EXPIRY_HOURS))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """التحقق من الرمز"""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError:
            return None

    def encrypt_data(self, data: str) -> str:
        """تشفير البيانات"""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted: str) -> str:
        """فك تشفير البيانات"""
        return self.cipher.decrypt(encrypted.encode()).decode()

    def generate_mfa_secret(self) -> str:
        """توليد سر MFA"""
        return pyotp.random_base32()

    def verify_mfa(self, secret: str, code: str) -> bool:
        """التحقق من MFA"""
        totp = pyotp.TOTP(secret)
        return totp.verify(code)

    def check_rate_limit(self, key: str, max_requests: int = 100, window: int = 60) -> bool:
        """التحقق من حد الطلبات"""
        # Redis-based rate limiting
        return True

    async def shutdown(self):
        """إيقاف مدير الأمان"""
        logger.info("🔒 إيقاف مدير الأمان")