from django.urls import path
from .views import BestLinksBinance, ProfitableLinksBinance


urlpatterns = [
    path('best-links-binance/', BestLinksBinance.as_view(), name='best-links-binance'),
    path('profitable-links-binance/', ProfitableLinksBinance.as_view(), name='profitable-links-binance'),
]