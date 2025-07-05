from decouple import config

KAFKA_BOOTSTRAP_SERVERS = config('KAFKA_BOOTSTRAP_SERVERS', default='localhost:9092')
STOCK_PRICE_TOPIC = 'stock_prices'
MARKET_TRENDS_TOPIC = 'market_trends'

# Kafka producer configuration
KAFKA_PRODUCER_CONFIG = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'client.id': 'stock-market-producer',
    'compression.type': 'lz4',
    'acks': 'all',
    'retries': 3,
    'batch.size': 32768,
    'linger.ms': 10,
}

# Kafka consumer configuration
KAFKA_CONSUMER_CONFIG = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'stock-market-consumer-group',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'max.poll.interval.ms': 300000,
}
