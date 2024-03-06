from django.urls import path
from .views import Home, ProfitableLinks


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('profitable-links/', ProfitableLinks.as_view(), name='profitable-links'),
]