import React from 'react'
import { NavLink } from 'react-router-dom'
import {
  HomeIcon,
  BanknotesIcon,
  CubeIcon,
  CogIcon,
  ClipboardDocumentCheckIcon,
  ChartBarIcon,
  CurrencyDollarIcon,
  UsersIcon,
  MegaphoneIcon,
  BriefcaseIcon,
  CpuChipIcon,
  ShieldCheckIcon,
  BeakerIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline'

const menuItems = [
  { path: '/', label: 'الرئيسية', icon: HomeIcon },
  { path: '/executive', label: 'التنفيذي', icon: BriefcaseIcon },
  { path: '/finance', label: 'المالية', icon: BanknotesIcon },
  { path: '/inventory', label: 'المخزون', icon: CubeIcon },
  { path: '/production', label: 'الإنتاج', icon: CogIcon },
  { path: '/accounting', label: 'المحاسبة', icon: ClipboardDocumentCheckIcon },
  { path: '/audit', label: 'التدقيق', icon: ShieldCheckIcon },
  { path: '/investment', label: 'الاستثمارات', icon: ChartBarIcon },
  { path: '/revenue', label: 'الإيرادات', icon: CurrencyDollarIcon },
  { path: '/hr', label: 'الموارد البشرية', icon: UsersIcon },
  { path: '/marketing', label: 'التسويق', icon: MegaphoneIcon },
  { path: '/ai-engine', label: 'محرك الذكاء', icon: CpuChipIcon },
  { path: '/settings', label: 'الإعدادات', icon: Cog6ToothIcon },
]

const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-enterprise-card border-l border-enterprise-border flex flex-col">
      <div className="p-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center">
            <CpuChipIcon className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold gradient-text">EnterpriseAI</h1>
            <p className="text-xs text-gray-400">OS v1.0</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 px-4 py-2 space-y-1 overflow-y-auto">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive
                  ? 'bg-primary-600/20 text-primary-400 border-r-2 border-primary-500'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span className="text-sm font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-enterprise-border">
        <div className="glass-card p-3">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-xs text-gray-400">11 وكيل نشط</span>
          </div>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
