import React from 'react'
import { useQuery } from 'react-query'
import {
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  BanknotesIcon,
  CubeIcon,
  UsersIcon,
  ChartPieIcon,
} from '@heroicons/react/24/outline'

const KPICard: React.FC<{ title: string; value: string; change: string; trend: 'up' | 'down'; icon: any }> = ({
  title,
  value,
  change,
  trend,
  icon: Icon,
}) => (
  <div className="glass-card p-6 hover-glow">
    <div className="flex items-start justify-between">
      <div>
        <p className="text-sm text-gray-400 mb-1">{title}</p>
        <p className="text-2xl font-bold text-white">{value}</p>
        <div className={`flex items-center gap-1 mt-2 ${trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
          {trend === 'up' ? <ArrowTrendingUpIcon className="w-4 h-4" /> : <ArrowTrendingDownIcon className="w-4 h-4" />}
          <span className="text-sm">{change}</span>
        </div>
      </div>
      <div className="p-3 bg-primary-500/10 rounded-lg">
        <Icon className="w-6 h-6 text-primary-400" />
      </div>
    </div>
  </div>
)

const AgentStatus: React.FC = () => {
  const { data } = useQuery('agents-status', async () => {
    const res = await fetch('/api/v1/ai/agents/status')
    return res.json()
  }, { refetchInterval: 5000 })

  return (
    <div className="glass-card p-6">
      <h3 className="text-lg font-semibold text-white mb-4">حالة الوكلاء الذكيين</h3>
      <div className="space-y-3">
        {data?.agents?.map((agent: any) => (
          <div key={agent.name} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
            <div className="flex items-center gap-3">
              <div className={`w-2 h-2 rounded-full ${agent.status === 'online' ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-sm text-white">{agent.name}</span>
            </div>
            <div className="flex items-center gap-4 text-xs text-gray-400">
              <span>المهام: {agent.tasks_processed}</span>
              <span>النجاح: {(agent.success_rate * 100).toFixed(0)}%</span>
            </div>
          </div>
        )) || (
          <div className="text-gray-400 text-sm">جاري التحميل...</div>
        )}
      </div>
    </div>
  )
}

const RecentActivity: React.FC = () => {
  const activities = [
    { time: 'منذ 5 دقائق', text: 'FinancialAgent: تنبؤ بالتدفق النقدي للربع القادم', type: 'success' },
    { time: 'منذ 12 دقيقة', text: 'InventoryAgent: كشف 3 منتجات نفدت من المخزون', type: 'warning' },
    { time: 'منذ 30 دقيقة', text: 'HRAgent: مرشح جديد بدرجة 87% - يُنصح بالتوظيف', type: 'info' },
    { time: 'منذ ساعة', text: 'AuditAgent: اكتمال التدقيق الشهري بدون ملاحظات', type: 'success' },
  ]

  return (
    <div className="glass-card p-6">
      <h3 className="text-lg font-semibold text-white mb-4">النشاط الأخير</h3>
      <div className="space-y-4">
        {activities.map((activity, i) => (
          <div key={i} className="flex items-start gap-3">
            <div className={`w-2 h-2 rounded-full mt-2 ${
              activity.type === 'success' ? 'bg-green-500' :
              activity.type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
            }`} />
            <div>
              <p className="text-sm text-white">{activity.text}</p>
              <p className="text-xs text-gray-400">{activity.time}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white mb-2">لوحة القيادة الرئيسية</h1>
        <p className="text-gray-400">نظرة شاملة على أداء المؤسسة</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="الإيرادات الشهرية"
          value="$2,850,000"
          change="+15%"
          trend="up"
          icon={BanknotesIcon}
        />
        <KPICard
          title="قيمة المخزون"
          value="$2,500,000"
          change="-3%"
          trend="down"
          icon={CubeIcon}
        />
        <KPICard
          title="الموظفين"
          value="248"
          change="+5"
          trend="up"
          icon={UsersIcon}
        />
        <KPICard
          title="هامش الربح"
          value="22%"
          change="+2%"
          trend="up"
          icon={ChartPieIcon}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AgentStatus />
        <RecentActivity />
      </div>

      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-4">التوصيات الذكية</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-primary-500/10 border border-primary-500/20 rounded-lg">
            <p className="text-primary-400 font-medium mb-2">💰 FinancialAgent</p>
            <p className="text-sm text-gray-300">الطلب المتوقع في ارتفاع 15% - زيادة المخزون 20%</p>
          </div>
          <div className="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
            <p className="text-yellow-400 font-medium mb-2">📦 InventoryAgent</p>
            <p className="text-sm text-gray-300">3 منتجات نفدت - إنشاء أوامر شراء عاجلة</p>
          </div>
          <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
            <p className="text-green-400 font-medium mb-2">👥 HRAgent</p>
            <p className="text-sm text-gray-300">مرشح ممتاز متاح - يُنصح بالتوظيف السريع</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
