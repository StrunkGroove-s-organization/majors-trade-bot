from django.urls import path
from .views import Home, HistoryLinksView


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('history-links/', HistoryLinksView.as_view(), name='history-links'),
]