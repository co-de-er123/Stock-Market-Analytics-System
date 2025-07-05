from django.urls import re_path
from . import views

websocket_urlpatterns = [
    re_path(r'^stock-updates/$', views.StockUpdateConsumer.as_asgi()),
]
