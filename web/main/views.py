from django.shortcuts import render, redirect
from django.views import View
from django.core.cache import cache

from .services import TrackingLinks
from .forms import CheckTickerForm
from count.services import CountBookTicker
from parsing.services import CheckPriceBinanceBySymbol


app_name = __package__


class MenuView:
    def menu_view(self, request):
        menu_items = [
            {'label': 'Связки', 'url': '/'},
            {'label': 'Проверить ticker', 'url': '/check-ticker/'},
        ]
        return menu_items


class Home(View, MenuView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        positive_links = cache.get(CountBookTicker().key_positive_links)
        context = {'positive_links': positive_links, 'menu_items': self.menu_view}
        return render(request, app_name + '/' + self.template_name, context)


class CheckTickerView(View, MenuView):
    template_name = 'check_ticker.html'

    def get(self, request, *args, **kwargs):
        form = CheckTickerForm()
        context = {'form': form, 'menu_items': self.menu_view}
        return render(request, app_name + '/' + self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = CheckTickerForm(request.POST)
        if not form.is_valid():
            return redirect('check-ticker')

        symbol = form.cleaned_data['ticker']
        info = CheckPriceBinanceBySymbol(symbol).main()
        context = {
            'form': form, 'info': info, 
            'ticker': symbol, 
            'menu_items': self.menu_view
        }
        return render(request, app_name + '/' + self.template_name, context)
    

class HistoryLinksView(View, MenuView):
    template_name = 'history_links.html'

    def get(self, request, *args, **kwargs):
        grouped_data = TrackingLinks().get_data()
        context = {'grouped_data': grouped_data}
        return render(request, app_name + '/' + self.template_name, context)
    
