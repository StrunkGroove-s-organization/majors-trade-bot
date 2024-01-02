from django.db import models


class OrderBookHistoryModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    spread = models.FloatField()

    first_symbol = models.CharField(max_length=255)
    first_ask_price = models.FloatField()
    first_bid_price = models.FloatField()
    first_ask_qty = models.FloatField()
    first_bid_qty = models.FloatField()
    first_order_book = models.JSONField(null=True)

    second_symbol = models.CharField(max_length=255)
    second_ask_price = models.FloatField()
    second_bid_price = models.FloatField()
    second_ask_qty = models.FloatField()
    second_bid_qty = models.FloatField()
    second_order_book = models.JSONField(null=True)

    third_symbol = models.CharField(max_length=255)
    third_ask_price = models.FloatField()
    third_bid_price = models.FloatField()
    third_ask_qty = models.FloatField()
    third_bid_qty = models.FloatField()
    third_order_book = models.JSONField(null=True)