#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - Investment Agent
وكيل الاستثمارات
"""

import logging
import numpy as np
from typing import Dict, Any, List
from datetime import datetime, timedelta

from ai_engine.agents.base_agent import BaseAgent, AgentConfig, Task, Plan, Step, StepResult, AgentResponse

logger = logging.getLogger(__name__)


class InvestmentAgent(BaseAgent):
    """وكيل الاستثمارات المتخصص"""

    def __init__(self):
        super().__init__(AgentConfig(
            name="InvestmentAgent",
            description="وكيل متخصص في تحليل الفرص الاستثمارية وإدارة المحافظ",
            capabilities=[
                "opportunity_analysis",
                "portfolio_optimization",
                "risk_assessment",
                "monte_carlo_simulation",
                "market_sentiment_analysis",
                "due_diligence",
                "asset_allocation",
                "performance_attribution"
            ],
            models=["portfolio-optimizer", "risk-model", "sentiment-analyzer"],
            data_sources=["market_data", "portfolio_holdings", "economic_indicators", "news_feeds"]
        ))

    async def plan(self, task: Task, context: Dict[str, Any]) -> Plan:
        if task.type == "portfolio_analysis":
            return Plan(steps=[
                Step("gather_holdings", {}),
                Step("calculate_metrics", {"sharpe": True, "sortino": True, "var": True}),
                Step("analyze_correlations", {}),
                Step("run_monte_carlo", {"simulations": 10000, "horizon": 252}),
                Step("optimize_allocation", {"objective": "max_sharpe"}),
                Step("generate_report", {"include_stress_test": True})
            ], estimated_time=60.0)
        elif task.type == "opportunity_screening":
            return Plan(steps=[
                Step("scan_market", {"universe": "all", "filters": task.data.get("filters", {})}),
                Step("fundamental_analysis", {"metrics": ["pe", "pb", "roe", "debt_ratio"]}),
                Step("technical_analysis", {"indicators": ["rsi", "macd", "bollinger"]}),
                Step("sentiment_scoring", {"sources": ["news", "social", "analyst"]}),
                Step("rank_opportunities", {}),
                Step("generate_watchlist", {})
            ], estimated_time=45.0)
        else:
            return Plan(steps=[
                Step("analyze_investment_request", {}),
                Step("gather_market_data", {}),
                Step("run_analysis", {}),
                Step("generate_recommendation", {})
            ], estimated_time=30.0)

    async def execute_step(self, step: Step) -> StepResult:
        if step.name == "run_monte_carlo":
            return StepResult(
                step_name="run_monte_carlo",
                success=True,
                data={
                    "simulations": 10000,
                    "expected_return": 0.12,
                    "volatility": 0.18,
                    "var_95": -0.05,
                    "cvar_95": -0.08,
                    "probability_of_profit": 0.72,
                    "worst_case": -0.35,
                    "best_case": 0.65
                }
            )
        elif step.name == "optimize_allocation":
            return StepResult(
                step_name="optimize_allocation",
                success=True,
                data={
                    "optimal_weights": {
                        "stocks": 0.55,
                        "bonds": 0.30,
                        "alternatives": 0.10,
                        "cash": 0.05
                    },
                    "expected_sharpe": 1.45,
                    "rebalancing_needed": True,
                    "rebalancing_trades": [
                        {"asset": "stocks", "action": "buy", "amount": 50000},
                        {"asset": "bonds", "action": "sell", "amount": 30000}
                    ]
                }
            )
        else:
            return StepResult(step_name=step.name, success=True, data={"status": "completed"})

    async def synthesize(self, task: Task, results: List[StepResult], context: Dict) -> AgentResponse:
        combined = {}
        for r in results:
            combined.update(r.data)

        insights = []
        recommendations = []
        warnings = []

        if "var_95" in combined:
            var = combined["var_95"]
            if var < -0.05:
                warnings.append(f"⚠️ VaR 95% = {var:.1%} - مخاطر مرتفعة")
                recommendations.append("🛡️ فكر في التحوط أو تقليل التعرض")

        if "rebalancing_needed" in combined and combined["rebalancing_needed"]:
            insights.append("📊 المحفظة تحتاج إعادة توازن")
            recommendations.append("🔄 نفذ صفقات إعادة التوازن المقترحة")

        return AgentResponse(
            task_id=task.id,
            agent_name=self.config.name,
            status="completed",
            result=combined,
            confidence=0.85,
            explanation="تم تحليل الاستثمارات وإعداد التوصيات",
            insights=insights,
            recommendations=recommendations,
            warnings=warnings
        )
