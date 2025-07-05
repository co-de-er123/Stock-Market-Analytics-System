import json
from kafka import KafkaConsumer
from kafka.structs import TopicPartition
from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from stock_analytics.models import StockPrice, MarketTrend
import numpy as np
from scipy.stats import linregress

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Kafka consumer for processing stock price updates'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.consumer.subscribe(['stock_prices'])

    def analyze_trend(self, prices):
        """Analyze market trend based on price history"""
        timestamps = np.array([p.timestamp.timestamp() for p in prices])
        prices = np.array([float(p.close_price) for p in prices])
        
        slope, _, r_value, _, _ = linregress(timestamps, prices)
        
        if slope > 0:
            trend_type = 'UPWARD'
        elif slope < 0:
            trend_type = 'DOWNWARD'
        else:
            trend_type = 'STABLE'
        
        return {
            'trend_type': trend_type,
            'strength': abs(slope),
            'confidence': r_value**2,
            'pattern': {
                'slope': slope,
                'r_value': r_value
            }
        }

    def handle(self, *args, **options):
        while True:
            try:
                for message in self.consumer:
                    try:
                        data = message.value
                        stock_id = data['stock_id']
                        timestamp = datetime.fromisoformat(data['timestamp'])
                        
                        with transaction.atomic():
                            # Create or update stock price
                            stock_price = StockPrice.objects.create(
                                stock_id=stock_id,
                                timestamp=timestamp,
                                open_price=data['open_price'],
                                high_price=data['high_price'],
                                low_price=data['low_price'],
                                close_price=data['close_price'],
                                volume=data['volume']
                            )
                            
                            # Analyze trend for the stock
                            recent_prices = StockPrice.objects.filter(
                                stock_id=stock_id,
                                timestamp__gte=timestamp - timedelta(hours=24)
                            ).order_by('timestamp')[:100]
                            
                            if len(recent_prices) >= 20:
                                trend_analysis = self.analyze_trend(recent_prices)
                                MarketTrend.objects.create(
                                    stock_id=stock_id,
                                    timestamp=timestamp,
                                    trend_type=trend_analysis['trend_type'],
                                    strength=trend_analysis['strength'],
                                    confidence=trend_analysis['confidence'],
                                    pattern=trend_analysis['pattern']
                                )
                            
                            logger.info(f"Processed price update for stock {stock_id}")
                    
                    except Exception as e:
                        logger.error(f"Error processing message: {str(e)}", exc_info=True)
                        continue
            
            except Exception as e:
                logger.error(f"Consumer error: {str(e)}", exc_info=True)
                self.consumer.close()
                break
