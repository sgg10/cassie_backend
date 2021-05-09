"""Trades Serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from cassie.trades.models import Trade

class TradeModelSerializer(serializers.ModelSerializer):
  """Trade model serializer."""

  open_price = serializers.FloatField()
  open_date = serializers.DateTimeField()
  close_price = serializers.FloatField()
  close_date = serializers.DateTimeField()

  stoploss = serializers.FloatField()
  takeprofit = serializers.FloatField()

  profit = serializers.FloatField()

  symbol = serializers.CharField()

  ticket = serializers.IntegerField()
  type_operation = serializers.CharField()

  class Meta:
    """Meta class."""
    model = Trade
    fields = (
      'open_price',
      'open_date',
      'close_price',
      'close_date',
      'stoploss',
      'takeprofit',
      'profit',
      'symbol',
      'ticket',
      'type_operation',
      'created',
      'modified'
    )
