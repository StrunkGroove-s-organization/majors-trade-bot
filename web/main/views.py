from django.shortcuts import render
from django.views import View

from count.services import CountBookTicker, AnalysisProfitLinks


app_name = __package__


class Menu:
    @staticmethod
    def menu_view():
        return [
            {'label': 'Связки', 'url_name': 'home'},
            {'label': 'Профитные связки', 'url_name': 'profitable-links'},
        ]


class Home(View, Menu):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        positive_links = CountBookTicker().positive_links
        context = {'positive_links': positive_links, 'menu': self.menu_view()}
        template_path = app_name + '/' + self.template_name
        return render(request, template_path, context)
    

class ProfitableLinks(View, Menu):
    template_name = 'profit_links.html'

    def get(self, request, *args, **kwargs):
        analysis_data = AnalysisProfitLinks().analysis_data
        context = {'grouped_data': analysis_data, 'menu': self.menu_view()}
        template_path = app_name + '/' + self.template_name
        return render(request, template_path, context)
