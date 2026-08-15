import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Finance from './pages/Finance'
import Inventory from './pages/Inventory'
import Production from './pages/Production'
import Accounting from './pages/Accounting'
import Audit from './pages/Audit'
import Investment from './pages/Investment'
import Revenue from './pages/Revenue'
import HR from './pages/HR'
import Marketing from './pages/Marketing'
import Executive from './pages/Executive'
import AIEngine from './pages/AIEngine'
import Settings from './pages/Settings'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="finance" element={<Finance />} />
        <Route path="inventory" element={<Inventory />} />
        <Route path="production" element={<Production />} />
        <Route path="accounting" element={<Accounting />} />
        <Route path="audit" element={<Audit />} />
        <Route path="investment" element={<Investment />} />
        <Route path="revenue" element={<Revenue />} />
        <Route path="hr" element={<HR />} />
        <Route path="marketing" element={<Marketing />} />
        <Route path="executive" element={<Executive />} />
        <Route path="ai-engine" element={<AIEngine />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  )
}

export default App
