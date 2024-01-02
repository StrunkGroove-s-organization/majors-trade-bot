from django.urls import path
from .views import Home, CheckTickerView, HistoryLinksView


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('check-ticker/', CheckTickerView.as_view(), name='check-ticker'),
    path('history-links/', HistoryLinksView.as_view(), name='history-links'),
]