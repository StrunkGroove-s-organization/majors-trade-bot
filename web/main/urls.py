from django.urls import path
from .views import Home, CheckTickerView


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('check-ticker/', CheckTickerView.as_view(), name='check-ticker'),
]