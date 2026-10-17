import { Plus } from 'lucide-react'

export default function Agents() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Agents</h1>
        <button className="flex items-center rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          <Plus className="h-5 w-5 mr-2" />
          Create Agent
        </button>
      </div>
      
      <div className="rounded-lg border bg-white shadow-sm dark:bg-gray-800">
        <div className="grid gap-4 p-6">
          {/* Agent cards */}
          {[
            { name: 'data-analyzer', framework: 'LangChain', status: 'deployed', trustTier: 3 },
            { name: 'customer-support', framework: 'AutoGPT', status: 'deployed', trustTier: 2 },
            { name: 'code-reviewer', framework: 'CrewAI', status: 'draft', trustTier: 4 },
          ].map((agent) => (
            <div
              key={agent.name}
              className="flex items-center justify-between rounded-lg border p-4 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <div>
                <h3 className="font-semibold">{agent.name}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {agent.framework} • Trust Tier {agent.trustTier}
                </p>
              </div>
              <div className="flex items-center space-x-4">
                <span
                  className={`rounded-full px-3 py-1 text-sm ${
                    agent.status === 'deployed'
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                  }`}
                >
                  {agent.status}
                </span>
                <button className="text-blue-600 hover:text-blue-700">View</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
