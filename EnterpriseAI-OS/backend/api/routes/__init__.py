#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - API Routes
نقاط النهاية
"""

from fastapi import APIRouter

from api.routes import auth, users, finance, inventory, production, accounting
from api.routes import audit, investment, revenue, hr, marketing, executive, ai

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(finance.router, prefix="/finance", tags=["Finance"])
router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
router.include_router(production.router, prefix="/production", tags=["Production"])
router.include_router(accounting.router, prefix="/accounting", tags=["Accounting"])
router.include_router(audit.router, prefix="/audit", tags=["Audit"])
router.include_router(investment.router, prefix="/investment", tags=["Investment"])
router.include_router(revenue.router, prefix="/revenue", tags=["Revenue"])
router.include_router(hr.router, prefix="/hr", tags=["HR"])
router.include_router(marketing.router, prefix="/marketing", tags=["Marketing"])
router.include_router(executive.router, prefix="/executive", tags=["Executive"])
router.include_router(ai.router, prefix="/ai", tags=["AI Engine"])
