from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Stock, StockPrice, MarketTrend, Alert, UserPortfolio, PortfolioStock
from .serializers import StockSerializer, StockPriceSerializer, MarketTrendSerializer, AlertSerializer, UserPortfolioSerializer, PortfolioStockSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

class StockPriceViewSet(viewsets.ModelViewSet):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer
    permission_classes = [IsAuthenticated]

class MarketTrendViewSet(viewsets.ModelViewSet):
    queryset = MarketTrend.objects.all()
    serializer_class = MarketTrendSerializer
    permission_classes = [IsAuthenticated]

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

class UserPortfolioViewSet(viewsets.ModelViewSet):
    queryset = UserPortfolio.objects.all()
    serializer_class = UserPortfolioSerializer
    permission_classes = [IsAuthenticated]

class PortfolioStockViewSet(viewsets.ModelViewSet):
    queryset = PortfolioStock.objects.all()
    serializer_class = PortfolioStockSerializer
    permission_classes = [IsAuthenticated]

class StockUpdateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()
            return

        await self.accept()
        self.group_name = f"stock_updates_{user.id}"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        stock_symbol = content.get('stock_symbol')
        if not stock_symbol:
            return

        stock = await Stock.objects.filter(symbol=stock_symbol).afirst()
        if not stock:
            return

        latest_price = await StockPrice.objects.filter(stock=stock).order_by('-timestamp').afirst()
        if latest_price:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'stock_update',
                    'stock_symbol': stock.symbol,
                    'price': str(latest_price.close_price),
                    'timestamp': latest_price.timestamp.isoformat()
                }
            )

    async def stock_update(self, event):
        await self.send_json(event)
