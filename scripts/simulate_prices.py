import json
import time
import random
from kafka import KafkaProducer
from datetime import datetime, timedelta
import logging
from stock_analytics.models import Stock

logger = logging.getLogger(__name__)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulate price changes based on historical volatility
VOLATILITY = {
    'AAPL': 0.02,
    'GOOGL': 0.03,
    'MSFT': 0.025,
    'AMZN': 0.035,
    'TSLA': 0.05
}

# Initial prices
INITIAL_PRICES = {
    'AAPL': 180.00,
    'GOOGL': 120.00,
    'MSFT': 350.00,
    'AMZN': 130.00,
    'TSLA': 250.00
}

def generate_price_change(price, volatility):
    """Generate random price change based on volatility"""
    change = price * volatility * (random.random() * 2 - 1)
    return price + change

def simulate_prices():
    """Simulate stock price updates"""
    current_prices = INITIAL_PRICES.copy()
    
    while True:
        current_time = datetime.now()
        
        for stock in Stock.objects.all():
            symbol = stock.symbol
            
            # Generate new price
            new_price = generate_price_change(current_prices[symbol], VOLATILITY[symbol])
            
            # Create price data
            price_data = {
                'stock_id': stock.id,
                'timestamp': current_time.isoformat(),
                'open_price': current_prices[symbol],
                'high_price': max(current_prices[symbol], new_price),
                'low_price': min(current_prices[symbol], new_price),
                'close_price': new_price,
                'volume': random.randint(10000, 100000)
            }
            
            # Send to Kafka
            producer.send('stock_prices', price_data)
            
            # Update current price
            current_prices[symbol] = new_price
            
            logger.info(f"Simulated price update for {symbol}: {new_price}")
            
        # Wait for next update
        time.sleep(60)  # Simulate every minute

if __name__ == '__main__':
    try:
        logger.info("Starting price simulation...")
        simulate_prices()
    except KeyboardInterrupt:
        logger.info("Stopping price simulation...")
        producer.close()
