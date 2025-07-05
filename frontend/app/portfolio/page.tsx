import { useState, useEffect } from 'react'
import { Table } from '@tanstack/react-table'
import { useQuery } from '@tanstack/react-query'
import { toast } from 'react-hot-toast'

const endpoint = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Portfolio() {
  const [portfolio, setPortfolio] = useState<any[]>([])
  const [selectedStock, setSelectedStock] = useState<string>('')
  const [quantity, setQuantity] = useState<number>(0)

  const { data: stocks } = useQuery({
    queryKey: ['stocks'],
    queryFn: () => fetch(`${endpoint}/api/stocks/`).then(res => res.json())
  })

  const { data: userPortfolio } = useQuery({
    queryKey: ['user-portfolio'],
    queryFn: () => fetch(`${endpoint}/api/portfolio/`).then(res => res.json())
  })

  useEffect(() => {
    if (userPortfolio) {
      setPortfolio(userPortfolio)
    }
  }, [userPortfolio])

  const handleAddToPortfolio = async () => {
    if (!selectedStock || quantity <= 0) return

    try {
      const response = await fetch(`${endpoint}/api/portfolio/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          stock_symbol: selectedStock,
          quantity: quantity
        })
      })

      if (!response.ok) throw new Error('Failed to add to portfolio')

      toast.success('Stock added to portfolio')
      setQuantity(0)
    } catch (error) {
      toast.error('Failed to add stock to portfolio')
    }
  }

  return (
    <div className="space-y-8">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Add to Portfolio</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="stock" className="block text-sm font-medium text-gray-700">
              Stock
            </label>
            <select
              id="stock"
              value={selectedStock}
              onChange={(e) => setSelectedStock(e.target.value)}
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
            <label htmlFor="quantity" className="block text-sm font-medium text-gray-700">
              Quantity
            </label>
            <input
              type="number"
              id="quantity"
              value={quantity}
              onChange={(e) => setQuantity(Number(e.target.value))}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
        </div>
        <button
          onClick={handleAddToPortfolio}
          className="mt-4 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Add to Portfolio
        </button>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Portfolio</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Stock
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Quantity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Current Price
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total Value
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {portfolio.map((item: any) => (
                <tr key={item.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">
                          {item.stock.name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {item.stock.symbol}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{item.quantity}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">${item.stock.current_price}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      ${item.quantity * item.stock.current_price}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      className="text-indigo-600 hover:text-indigo-900"
                      onClick={() => {
                        // Add sell functionality
                      }}
                    >
                      Sell
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
