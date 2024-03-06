from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import CountBookTicker


class PositiveLinksBinance(APIView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        positive_links = CountBookTicker.positive_links

        if positive_links is not None:
            return Response({'data': positive_links})
        return Response({'error': 'Data not found in the cache'}, status=404)