from django.shortcuts import render
from django.views import View

from .services import TrackingLinks
from count.services import CountBookTicker


app_name = __package__


class MenuView:
    def menu_view(self, request):
        menu_items = [
            {'label': 'Связки', 'url': '/'},
        ]
        return menu_items


class Home(View, MenuView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        positive_links = CountBookTicker().get_count_links()
        context = {'positive_links': positive_links, 'menu_items': self.menu_view}
        return render(request, app_name + '/' + self.template_name, context)
    

class HistoryLinksView(View, MenuView):
    template_name = 'history_links.html'

    def get(self, request, *args, **kwargs):
        grouped_data = TrackingLinks().get_data()
        context = {'grouped_data': grouped_data}
        return render(request, app_name + '/' + self.template_name, context)
    
