import json
import requests
from django.core.management.base import BaseCommand
from stock_analytics.models import Stock

class Command(BaseCommand):
    help = 'Populate database with stock data'

    def handle(self, *args, **options):
        # Example stock data - in production, this would come from an API
        stock_data = [
            {
                'symbol': 'AAPL',
                'name': 'Apple Inc.',
                'exchange': 'NASDAQ',
                'sector': 'Technology',
                'industry': 'Consumer Electronics'
            },
            {
                'symbol': 'GOOGL',
                'name': 'Alphabet Inc.',
                'exchange': 'NASDAQ',
                'sector': 'Technology',
                'industry': 'Internet Services'
            },
            {
                'symbol': 'MSFT',
                'name': 'Microsoft Corporation',
                'exchange': 'NASDAQ',
                'sector': 'Technology',
                'industry': 'Software'
            },
            {
                'symbol': 'AMZN',
                'name': 'Amazon.com, Inc.',
                'exchange': 'NASDAQ',
                'sector': 'Consumer Cyclical',
                'industry': 'Internet Retail'
            },
            {
                'symbol': 'TSLA',
                'name': 'Tesla, Inc.',
                'exchange': 'NASDAQ',
                'sector': 'Consumer Cyclical',
                'industry': 'Auto Manufacturers'
            }
        ]

        for stock in stock_data:
            Stock.objects.create(**stock)
            self.stdout.write(self.style.SUCCESS(f'Successfully created stock {stock["symbol"]}'))
