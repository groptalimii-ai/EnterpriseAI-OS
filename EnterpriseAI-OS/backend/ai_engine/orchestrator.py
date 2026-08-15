#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - AI Orchestrator
منسق الوكلاء الذكي
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from ai_engine.agents.base_agent import BaseAgent, AgentConfig, Task, AgentResponse

logger = logging.getLogger(__name__)


class AIOrchestrator:
    """منسق الوكلاء الذكي"""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.processing = False
        self.initialized = False

    async def initialize(self):
        """تهيئة المنسق"""
        logger.info("🔧 تهيئة منسق الذكاء الاصطناعي...")

        # تسجيل الوكلاء
        await self._register_agents()

        # تهيئة كل وكيل
        for agent in self.agents.values():
            await agent.initialize()

        # بدء معالج المهام
        self.processing = True
        asyncio.create_task(self._process_task_queue())

        self.initialized = True
        logger.info(f"✅ تم تهيئة {len(self.agents)} وكيل")

    async def _register_agents(self):
        """تسجيل الوكلاء"""
        from ai_agents.financial_agent.agent import FinancialAgent
        from ai_agents.inventory_agent.agent import InventoryAgent
        from ai_agents.production_agent.agent import ProductionAgent
        from ai_agents.accounting_agent.agent import AccountingAgent
        from ai_agents.audit_agent.agent import AuditAgent
        from ai_agents.investment_agent.agent import InvestmentAgent
        from ai_agents.revenue_agent.agent import RevenueAgent
        from ai_agents.hr_agent.agent import HRAgent
        from ai_agents.marketing_agent.agent import MarketingAgent
        from ai_agents.executive_agent.agent import ExecutiveAgent
        from ai_agents.cross_department_agent.agent import CrossDepartmentAgent

        agents = [
            FinancialAgent(),
            InventoryAgent(),
            ProductionAgent(),
            AccountingAgent(),
            AuditAgent(),
            InvestmentAgent(),
            RevenueAgent(),
            HRAgent(),
            MarketingAgent(),
            ExecutiveAgent(),
            CrossDepartmentAgent(),
        ]

        for agent in agents:
            self.agents[agent.config.name] = agent

    async def route_task(self, task: Task) -> AgentResponse:
        """توجيه مهمة للوكيل المناسب"""

        # 1. تحليل المهمة
        agent = self.select_optimal_agent(task)

        if not agent:
            return AgentResponse(
                task_id=task.id,
                agent_name="orchestrator",
                status="failed",
                result={"error": "No suitable agent found"},
                confidence=0.0,
                explanation="لم يتم العثور على وكيل مناسب لهذه المهمة"
            )

        # 2. تنفيذ المهمة
        logger.info(f"🎯 توجيه المهمة {task.type} إلى {agent.config.name}")
        response = await agent.execute(task)

        # 3. إذا كانت المهمة متعددة الأقسام
        if task.type.startswith("cross_"):
            response = await self._coordinate_cross_department(task, response)

        return response

    def select_optimal_agent(self, task: Task) -> Optional[BaseAgent]:
        """اختيار الوكيل الأمثل"""

        # خريطة المهام للوكلاء
        task_agent_map = {
            "forecast": "FinancialAgent",
            "budget": "FinancialAgent",
            "cash_flow": "FinancialAgent",
            "inventory_check": "InventoryAgent",
            "demand_prediction": "InventoryAgent",
            "production_schedule": "ProductionAgent",
            "quality_check": "ProductionAgent",
            "journal_entry": "AccountingAgent",
            "reconciliation": "AccountingAgent",
            "audit": "AuditAgent",
            "fraud_detection": "AuditAgent",
            "investment_analysis": "InvestmentAgent",
            "portfolio": "InvestmentAgent",
            "pricing": "RevenueAgent",
            "revenue_forecast": "RevenueAgent",
            "recruitment": "HRAgent",
            "performance": "HRAgent",
            "campaign": "MarketingAgent",
            "sentiment": "MarketingAgent",
            "executive_report": "ExecutiveAgent",
            "strategy": "ExecutiveAgent",
        }

        agent_name = task_agent_map.get(task.type)
        if agent_name and agent_name in self.agents:
            return self.agents[agent_name]

        # البحث عن وكيل بناءً على القسم
        for agent in self.agents.values():
            if task.department.lower() in agent.config.name.lower():
                return agent

        # الوكيل المتعدد الأقسام كاحتياطي
        return self.agents.get("CrossDepartmentAgent")

    async def _coordinate_cross_department(self, task: Task, initial_response: AgentResponse) -> AgentResponse:
        """تنسيق بين الأقسام"""

        # جمع المدخلات من وكلاء متعددين
        responses = [initial_response]

        # إذا كانت مهمة شراء، نحتاج مدخلات من المخزون والمالية
        if task.type == "purchase_request":
            inventory_agent = self.agents.get("InventoryAgent")
            financial_agent = self.agents.get("FinancialAgent")

            if inventory_agent:
                inventory_task = Task(
                    id=f"{task.id}_inventory",
                    type="inventory_check",
                    data=task.data,
                    user_id=task.user_id,
                    department="inventory"
                )
                responses.append(await inventory_agent.execute(inventory_task))

            if financial_agent:
                financial_task = Task(
                    id=f"{task.id}_financial",
                    type="budget_check",
                    data=task.data,
                    user_id=task.user_id,
                    department="finance"
                )
                responses.append(await financial_agent.execute(financial_task))

        # دمج النتائج
        merged = self._merge_responses(responses)
        return merged

    def _merge_responses(self, responses: List[AgentResponse]) -> AgentResponse:
        """دمج الاستجابات"""

        combined_result = {}
        all_insights = []
        all_recommendations = []
        all_warnings = []
        min_confidence = 1.0

        for resp in responses:
            combined_result.update(resp.result)
            all_insights.extend(resp.insights)
            all_recommendations.extend(resp.recommendations)
            all_warnings.extend(resp.warnings)
            min_confidence = min(min_confidence, resp.confidence)

        return AgentResponse(
            task_id=responses[0].task_id,
            agent_name="CrossDepartmentAgent",
            status="completed",
            result=combined_result,
            confidence=min_confidence,
            explanation="تم التنسيق بين الأقسام",
            insights=all_insights,
            recommendations=all_recommendations,
            warnings=all_warnings
        )

    async def _process_task_queue(self):
        """معالج قائمة انتظار المهام"""
        while self.processing:
            try:
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                await self.route_task(task)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing task: {e}")

    async def get_agents_status(self) -> Dict[str, Any]:
        """حالة الوكلاء"""
        status = {}
        for name, agent in self.agents.items():
            status[name] = await agent.get_status()
        return status

    async def train_agent(self, agent_id: str, training_data: Any) -> Dict[str, Any]:
        """تدريب وكيل"""
        agent = self.agents.get(agent_id)
        if not agent:
            return {"error": f"Agent {agent_id} not found"}

        # التدريب
        return {"status": "training_started", "agent": agent_id}

    async def notify_agents(self, event: Any):
        """إخطار الوكلاء بحدث"""
        for agent in self.agents.values():
            # إذا كان الحدث يخص الوكيل
            if hasattr(event, 'aggregate_type'):
                if event.aggregate_type in agent.config.data_sources:
                    asyncio.create_task(self._notify_agent(agent, event))

    async def _notify_agent(self, agent: BaseAgent, event: Any):
        """إخطار وكيل محدد"""
        logger.debug(f"📢 إخطار {agent.config.name} بحدث {event.event_type}")
        # يمكن للوكيل اتخاذ إجراء بناءً على الحدث

    async def shutdown(self):
        """إيقاف المنسق"""
        logger.info("🛑 إيقاف منسق الذكاء الاصطناعي...")
        self.processing = False

        for agent in self.agents.values():
            await agent.shutdown()

        logger.info("✅ تم إيقاف المنسق")
