export default function Executions() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Executions</h1>
      
      <div className="rounded-lg border bg-white shadow-sm dark:bg-gray-800">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="px-6 py-3 text-left text-sm font-semibold">ID</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Agent</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Status</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Duration</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Cost</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Time</th>
              </tr>
            </thead>
            <tbody>
              {[
                { id: 'exec-001', agent: 'data-analyzer', status: 'completed', duration: '2.3s', cost: '$0.05', time: '2 min ago' },
                { id: 'exec-002', agent: 'customer-support', status: 'completed', duration: '5.1s', cost: '$0.12', time: '5 min ago' },
                { id: 'exec-003', agent: 'code-reviewer', status: 'failed', duration: '1.2s', cost: '$0.02', time: '10 min ago' },
              ].map((execution) => (
                <tr key={execution.id} className="border-b hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 text-sm">{execution.id}</td>
                  <td className="px-6 py-4 text-sm">{execution.agent}</td>
                  <td className="px-6 py-4 text-sm">
                    <span
                      className={`rounded-full px-2 py-1 text-xs ${
                        execution.status === 'completed'
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                          : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                      }`}
                    >
                      {execution.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm">{execution.duration}</td>
                  <td className="px-6 py-4 text-sm">{execution.cost}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{execution.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
