from django.urls import path
from .views import PositiveLinksBinance


urlpatterns = [
    path('positive-links-binance/', PositiveLinksBinance.as_view(), name='positive-links-binance'),
]