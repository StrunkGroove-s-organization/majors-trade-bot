from django import forms


class CheckTickerForm(forms.Form):
    ticker = forms.CharField(label="Введите ticker (пример: 'BTCUSDT'):")