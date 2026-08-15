import React from 'react'
import { BellIcon, MagnifyingGlassIcon, UserCircleIcon } from '@heroicons/react/24/outline'

const Header: React.FC = () => {
  return (
    <header className="h-16 bg-enterprise-card border-b border-enterprise-border flex items-center justify-between px-6">
      <div className="flex items-center gap-4 flex-1">
        <div className="relative">
          <MagnifyingGlassIcon className="w-5 h-5 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="بحث ذكي..."
            className="bg-enterprise-dark border border-enterprise-border rounded-lg pr-10 pl-4 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-primary-500 w-80"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="relative p-2 text-gray-400 hover:text-white transition-colors">
          <BellIcon className="w-6 h-6" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </button>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <p className="text-sm font-medium text-white">مدير النظام</p>
            <p className="text-xs text-gray-400">الإدارة التنفيذية</p>
          </div>
          <UserCircleIcon className="w-10 h-10 text-gray-400" />
        </div>
      </div>
    </header>
  )
}

export default Header
