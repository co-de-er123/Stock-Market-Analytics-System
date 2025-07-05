import { useState, useEffect } from 'react'
import { Table } from '@tanstack/react-table'
import { useQuery, useMutation } from '@tanstack/react-query'
import { toast } from 'react-hot-toast'

const endpoint = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Alerts() {
  const [alerts, setAlerts] = useState<any[]>([])
  const [newAlert, setNewAlert] = useState({
    stock_symbol: '',
    price_threshold: 0,
    condition: '>',
  })

  const { data: stocks } = useQuery({
    queryKey: ['stocks'],
    queryFn: () => fetch(`${endpoint}/api/stocks/`).then(res => res.json())
  })

  const { data: userAlerts } = useQuery({
    queryKey: ['user-alerts'],
    queryFn: () => fetch(`${endpoint}/api/alerts/`).then(res => res.json())
  })

  useEffect(() => {
    if (userAlerts) {
      setAlerts(userAlerts)
    }
  }, [userAlerts])

  const createAlert = useMutation({
    mutationFn: async (alert: any) => {
      const response = await fetch(`${endpoint}/api/alerts/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(alert)
      })
      return response.json()
    },
    onSuccess: () => {
      toast.success('Alert created successfully')
    },
    onError: () => {
      toast.error('Failed to create alert')
    }
  })

  const deleteAlert = useMutation({
    mutationFn: async (id: number) => {
      const response = await fetch(`${endpoint}/api/alerts/${id}/`, {
        method: 'DELETE'
      })
      return response.json()
    },
    onSuccess: () => {
      toast.success('Alert deleted successfully')
    },
    onError: () => {
      toast.error('Failed to delete alert')
    }
  })

  const handleCreateAlert = () => {
    if (!newAlert.stock_symbol || !newAlert.price_threshold) return

    createAlert.mutate(newAlert)
    setNewAlert({
      stock_symbol: '',
      price_threshold: 0,
      condition: '>'
    })
  }

  return (
    <div className="space-y-8">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Create Alert</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="stock" className="block text-sm font-medium text-gray-700">
              Stock
            </label>
            <select
              id="stock"
              value={newAlert.stock_symbol}
              onChange={(e) => setNewAlert({ ...newAlert, stock_symbol: e.target.value })}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
            >
              <option value="">Select a stock</option>
              {stocks?.map((stock: any) => (
                <option key={stock.symbol} value={stock.symbol}>
                  {stock.name} ({stock.symbol})
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="threshold" className="block text-sm font-medium text-gray-700">
              Price Threshold
            </label>
            <input
              type="number"
              id="threshold"
              value={newAlert.price_threshold}
              onChange={(e) => setNewAlert({ ...newAlert, price_threshold: Number(e.target.value) })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
          <div>
            <label htmlFor="condition" className="block text-sm font-medium text-gray-700">
              Condition
            </label>
            <select
              id="condition"
              value={newAlert.condition}
              onChange={(e) => setNewAlert({ ...newAlert, condition: e.target.value })}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
            >
              <option value="">Select condition</option>
              <option value=">">Above</option>
              <option value="<">Below</option>
              <option value="==">Equal to</option>
            </select>
          </div>
        </div>
        <button
          onClick={handleCreateAlert}
          className="mt-4 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Create Alert
        </button>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Alerts</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Stock
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Condition
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Price Threshold
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {alerts.map((alert: any) => (
                <tr key={alert.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{alert.stock.name}</div>
                    <div className="text-sm text-gray-500">{alert.stock.symbol}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {alert.condition === '>' ? 'Above' : 
                       alert.condition === '<' ? 'Below' : 'Equal to'}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">${alert.price_threshold}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      alert.is_triggered ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                    }`}>
                      {alert.is_triggered ? 'Triggered' : 'Active'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => deleteAlert.mutate(alert.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
