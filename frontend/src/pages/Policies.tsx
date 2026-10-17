import { Plus } from 'lucide-react'

export default function Policies() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Policies</h1>
        <button className="flex items-center rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          <Plus className="h-5 w-5 mr-2" />
          Create Policy
        </button>
      </div>
      
      <div className="rounded-lg border bg-white shadow-sm dark:bg-gray-800">
        <div className="grid gap-4 p-6">
          {[
            { name: 'default-policy', version: '1.0.0', active: true },
            { name: 'strict-security', version: '2.1.0', active: true },
            { name: 'development', version: '0.5.0', active: false },
          ].map((policy) => (
            <div
              key={policy.name}
              className="flex items-center justify-between rounded-lg border p-4 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <div>
                <h3 className="font-semibold">{policy.name}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Version {policy.version}</p>
              </div>
              <div className="flex items-center space-x-4">
                <span
                  className={`rounded-full px-3 py-1 text-sm ${
                    policy.active
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                  }`}
                >
                  {policy.active ? 'Active' : 'Inactive'}
                </span>
                <button className="text-blue-600 hover:text-blue-700">Edit</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
