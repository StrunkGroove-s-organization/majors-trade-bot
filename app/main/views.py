from django.shortcuts import render
from django.views import View
from django.core.cache import cache

from parsing.services import RedisClass


app_name = __package__


class Home(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        positive_links = cache.get(RedisClass().key_positive_links)
        context = {'positive_links': positive_links}
        return render(request, app_name + '/' + self.template_name, context)

