from django.db import models
from django.utils import timezone
from django.core.cache import cache
import json

class Stock(models.Model):
    class Meta:
        app_label = 'stock_analytics'
    
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    exchange = models.CharField(max_length=50)
    sector = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

class StockPrice(models.Model):
    class Meta:
        app_label = 'stock_analytics'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['stock', 'timestamp']),
        ]
    
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='prices')
    timestamp = models.DateTimeField(db_index=True)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.symbol} - {self.timestamp}"

class MarketTrend(models.Model):
    class Meta:
        app_label = 'stock_analytics'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['stock', 'timestamp']),
        ]
    
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='trends')
    timestamp = models.DateTimeField(db_index=True)
    trend_type = models.CharField(max_length=50, choices=[
        ('UPWARD', 'Upward Trend'),
        ('DOWNWARD', 'Downward Trend'),
        ('STABLE', 'Stable')
    ])
    strength = models.FloatField()
    confidence = models.FloatField()
    pattern = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.symbol} - {self.trend_type} ({self.timestamp})"

class Alert(models.Model):
    class Meta:
        app_label = 'stock_analytics'
        ordering = ['-created_at']
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='alerts')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='alerts')
    threshold_type = models.CharField(max_length=10, choices=[
        ('PRICE', 'Price'),
        ('VOLUME', 'Volume'),
        ('TREND', 'Trend')
    ])
    threshold_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_triggered = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Alert for {self.user.username} on {self.stock.symbol}"

class UserPortfolio(models.Model):
    class Meta:
        app_label = 'stock_analytics'
    
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='portfolio')
    total_value = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio of {self.user.username}"

class PortfolioStock(models.Model):
    class Meta:
        app_label = 'stock_analytics'
        unique_together = ('portfolio', 'stock')
    
    portfolio = models.ForeignKey(UserPortfolio, on_delete=models.CASCADE, related_name='stocks')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.portfolio.user.username} - {self.stock.symbol}"
