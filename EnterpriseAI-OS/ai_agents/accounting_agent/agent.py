#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - Accounting Agent
وكيل المحاسبة
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

from ai_engine.agents.base_agent import BaseAgent, AgentConfig, Task, Plan, Step, StepResult, AgentResponse

logger = logging.getLogger(__name__)


class AccountingAgent(BaseAgent):
    """وكيل المحاسبة المتخصص"""

    def __init__(self):
        super().__init__(AgentConfig(
            name="AccountingAgent",
            description="وكيل متخصص في المحاسبة التلقائية والتصنيف الذكي",
            capabilities=[
                "transaction_classification",
                "bank_reconciliation",
                "invoice_processing",
                "tax_compliance",
                "journal_entry_automation",
                "financial_statement_preparation",
                "variance_analysis",
                "audit_trail_generation"
            ],
            models=["accounting-bert", "invoice-parser"],
            data_sources=["transactions", "invoices", "bank_statements", "chart_of_accounts"]
        ))

    async def plan(self, task: Task, context: Dict[str, Any]) -> Plan:
        if task.type == "journal_entry":
            return Plan(steps=[
                Step("analyze_transaction", {}),
                Step("classify_accounts", {"chart_of_accounts": True}),
                Step("calculate_amounts", {"vat": True}),
                Step("validate_entry", {"debit_credit_balance": True}),
                Step("post_to_ledger", {}),
                Step("generate_audit_trail", {})
            ], estimated_time=15.0)
        elif task.type == "bank_reconciliation":
            return Plan(steps=[
                Step("fetch_bank_statements", {"period": "current_month"}),
                Step("fetch_ledger_entries", {"period": "current_month"}),
                Step("match_transactions", {"tolerance": 0.01}),
                Step("identify_discrepancies", {}),
                Step("suggest_adjustments", {}),
                Step("generate_reconciliation_report", {})
            ], estimated_time=25.0)
        else:
            return Plan(steps=[
                Step("analyze_accounting_request", {}),
                Step("process_data", {}),
                Step("generate_output", {})
            ], estimated_time=15.0)

    async def execute_step(self, step: Step) -> StepResult:
        if step.name == "classify_accounts":
            return StepResult(
                step_name="classify_accounts",
                success=True,
                data={
                    "debit_account": "6100 - Office Expenses",
                    "credit_account": "1100 - Cash",
                    "vat_account": "2200 - VAT Payable",
                    "confidence": 0.96
                }
            )
        elif step.name == "match_transactions":
            return StepResult(
                step_name="match_transactions",
                success=True,
                data={
                    "matched": 245,
                    "unmatched": 3,
                    "match_rate": 0.988,
                    "unmatched_items": [
                        {"bank": "Deposit 5000", "ledger": None, "suggestion": "Missing receipt"},
                        {"bank": None, "ledger": "Transfer 1200", "suggestion": "Pending clearance"}
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

        if "unmatched" in combined and combined["unmatched"] > 0:
            warnings.append(f"⚠️ {combined['unmatched']} معاملة غير متطابقة")
            recommendations.append("🔍 راجع المعاملات غير المتطابقة يدوياً")

        if "confidence" in combined and combined["confidence"] < 0.90:
            warnings.append("⚠️ ثقة التصنيف منخفضة - تحتاج مراجعة")

        return AgentResponse(
            task_id=task.id,
            agent_name=self.config.name,
            status="completed",
            result=combined,
            confidence=0.93,
            explanation="تمت المعالجة المحاسبية بنجاح",
            insights=insights,
            recommendations=recommendations,
            warnings=warnings
        )
