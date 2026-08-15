# 📚 API Reference

## نقاط النهاية

### Authentication
```
POST /api/v1/auth/login
POST /api/v1/auth/register
POST /api/v1/auth/refresh
POST /api/v1/auth/mfa/verify
```

### AI Engine
```
POST /api/v1/ai/query
GET  /api/v1/ai/agents/status
POST /api/v1/ai/agents/{id}/train
GET  /api/v1/ai/models
```

### Finance
```
POST /api/v1/finance/forecast/cash-flow
POST /api/v1/finance/optimize/budget
GET  /api/v1/finance/reports/{type}
GET  /api/v1/finance/kpis
```

### Inventory
```
POST /api/v1/inventory/forecast/demand
GET  /api/v1/inventory/status
GET  /api/v1/inventory/suppliers
```

### WebSocket
```
WS /ws
```

## نماذج الطلبات

### AI Query
```json
{
  "query": "تنبؤ بالتدفق النقدي للربع القادم",
  "agent_type": "financial",
  "department": "finance",
  "context": {}
}
```

### AI Response
```json
{
  "task_id": "task-123",
  "agent_name": "FinancialAgent",
  "status": "completed",
  "result": {},
  "confidence": 0.92,
  "explanation": "...",
  "insights": [],
  "recommendations": [],
  "warnings": []
}
```
