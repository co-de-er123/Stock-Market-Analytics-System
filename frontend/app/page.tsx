import { useEffect, useState } from 'react'
import { Line } from 'react-chartjs-2'
import socketIOClient from 'socket.io-client'
import { toast } from 'react-hot-toast'

const endpoint = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [stocks, setStocks] = useState<any[]>([])
  const [socket, setSocket] = useState<any>(null)
  const [selectedStock, setSelectedStock] = useState<string>('AAPL')
  const [chartData, setChartData] = useState<any>({})

  useEffect(() => {
    // Fetch initial stock data
    fetch(`${endpoint}/api/stocks/`)
      .then(response => response.json())
      .then(data => setStocks(data))
      .catch(error => console.error('Error:', error))

    // Connect to WebSocket
    const ws = socketIOClient(endpoint)
    setSocket(ws)

    // Listen for stock updates
    ws.on('stock_update', (data: any) => {
      if (data.symbol === selectedStock) {
        const newPrice = data.price
        const newData = {
          labels: [...chartData.labels, new Date().toLocaleTimeString()],
          datasets: [{
            ...chartData.datasets[0],
            data: [...chartData.datasets[0].data, newPrice]
          }]
        }
        setChartData(newData)
      }
    })

    return () => {
      ws.disconnect()
    }
  }, [])

  const handleStockSelect = (symbol: string) => {
    setSelectedStock(symbol)
    setChartData({
      labels: [],
      datasets: [{
        label: symbol,
        data: [],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    })
  }

  return (
    <div className="space-y-8">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Stock Market Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {stocks.map((stock: any) => (
            <div
              key={stock.symbol}
              className={`p-4 rounded-lg cursor-pointer transition-colors ${
                selectedStock === stock.symbol ? 'bg-indigo-50' : 'hover:bg-gray-50'
              }`}
              onClick={() => handleStockSelect(stock.symbol)}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-medium text-gray-900">{stock.name}</h3>
                  <p className="text-sm text-gray-500">{stock.symbol}</p>
                </div>
                <div className="text-right">
                  <p className="text-xl font-bold text-gray-900">${stock.current_price}</p>
                  <p
                    className={`text-sm ${
                      stock.change > 0 ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    {stock.change > 0 ? '+' : ''}{stock.change}%
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Price Chart</h2>
        <div className="h-[400px]">
          <Line data={chartData} />
        </div>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Market Trends</h2>
        <div className="space-y-4">
          {/* Add market trend indicators here */}
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span className="text-sm text-gray-500">Bullish Trend</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
            <span className="text-sm text-gray-500">Bearish Trend</span>
          </div>
        </div>
      </div>
    </div>
  )
}
