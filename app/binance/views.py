from django.http import HttpResponse
from django.views import View

from .tasks import task_start

class Start(View):
    def get(self, request, *args, **kwargs):
        task_start.delay()
        return HttpResponse("Задача запущена!")


