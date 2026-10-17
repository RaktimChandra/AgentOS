import { Outlet, Link } from 'react-router-dom'
import { Bot, Shield, Play, BarChart3, Settings } from 'lucide-react'

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 z-10 h-full w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
        <div className="flex h-16 items-center border-b border-gray-200 dark:border-gray-700 px-6">
          <Bot className="h-6 w-6 text-blue-600" />
          <span className="ml-2 text-xl font-bold">AgentOS</span>
        </div>
        
        <nav className="p-4 space-y-2">
          <Link
            to="/"
            className="flex items-center rounded-lg px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <BarChart3 className="h-5 w-5 mr-3" />
            Dashboard
          </Link>
          <Link
            to="/agents"
            className="flex items-center rounded-lg px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <Bot className="h-5 w-5 mr-3" />
            Agents
          </Link>
          <Link
            to="/policies"
            className="flex items-center rounded-lg px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <Shield className="h-5 w-5 mr-3" />
            Policies
          </Link>
          <Link
            to="/executions"
            className="flex items-center rounded-lg px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <Play className="h-5 w-5 mr-3" />
            Executions
          </Link>
          <Link
            to="/settings"
            className="flex items-center rounded-lg px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <Settings className="h-5 w-5 mr-3" />
            Settings
          </Link>
        </nav>
      </aside>

      {/* Main content */}
      <main className="ml-64 p-8">
        <Outlet />
      </main>
    </div>
  )
}
