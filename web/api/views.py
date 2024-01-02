from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from count.services import CountBookTicker
from django.views.decorators.csrf import csrf_exempt


class BestLinksBinance(APIView):

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        best_links = cache.get(CountBookTicker().key_positive_links)

        if best_links is not None:
            return Response({'data': best_links})
        return Response({'error': 'Data not found in the cache'}, status=404)