from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'stocks', views.StockViewSet)
router.register(r'prices', views.StockPriceViewSet)
router.register(r'trends', views.MarketTrendViewSet)
router.register(r'alerts', views.AlertViewSet)
router.register(r'portfolios', views.UserPortfolioViewSet)
router.register(r'portfolio-stocks', views.PortfolioStockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
