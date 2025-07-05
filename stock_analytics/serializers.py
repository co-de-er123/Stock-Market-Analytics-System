from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Stock, StockPrice, MarketTrend, Alert, UserPortfolio, PortfolioStock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'symbol', 'name', 'exchange', 'sector', 'industry', 'created_at', 'updated_at']

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = ['id', 'stock', 'timestamp', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'created_at']

class MarketTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketTrend
        fields = ['id', 'stock', 'timestamp', 'trend_type', 'strength', 'confidence', 'pattern', 'created_at']

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'user', 'stock', 'threshold_type', 'threshold_value', 'is_active', 'created_at', 'last_triggered']

class PortfolioStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioStock
        fields = ['id', 'portfolio', 'stock', 'quantity', 'average_price', 'created_at']

class UserPortfolioSerializer(serializers.ModelSerializer):
    stocks = PortfolioStockSerializer(many=True, read_only=True)

    class Meta:
        model = UserPortfolio
        fields = ['id', 'user', 'total_value', 'created_at', 'updated_at', 'stocks']
