from django.urls import path
from .views import BestLinksBinance


urlpatterns = [
    path('best-links-binance/', BestLinksBinance.as_view(), name='best-links-binance'),
]