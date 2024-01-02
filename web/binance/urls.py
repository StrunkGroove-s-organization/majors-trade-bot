from django.urls import path
from .views import Start

urlpatterns = [
    path('', Start.as_view(), name='start'),
]