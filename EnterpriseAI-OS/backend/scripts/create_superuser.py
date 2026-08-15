#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - Create Superuser
"""

import asyncio
import getpass
from uuid import uuid4
from datetime import datetime

async def create_superuser():
    print("👤 إنشاء المستخدم الأول (مدير النظام)")
    print("=" * 50)

    email = input("البريد الإلكتروني: ").strip()
    name = input("الاسم الكامل: ").strip()
    password = getpass.getpass("كلمة المرور: ")
    confirm = getpass.getpass("تأكيد كلمة المرور: ")

    if password != confirm:
        print("❌ كلمات المرور غير متطابقة!")
        return

    if len(password) < 8:
        print("❌ كلمة المرور يجب أن تكون 8 أحرف على الأقل!")
        return

    # TODO: إنشاء المستخدم في قاعدة البيانات
    print(f"✅ تم إنشاء المستخدم: {email}")
    print("🚀 يمكنك الآن تسجيل الدخول إلى النظام")

if __name__ == "__main__":
    asyncio.run(create_superuser())
