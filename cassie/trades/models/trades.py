"""Trades models."""

# Django
from django.db import models

# Utilities
from cassie.utils.models import CassieModel

class Trade(CassieModel):
  """Trade Model.
    Trade is a Glahad bot operation with all
    information about this operation. Each Trade
    is part of a complete report.
  """

  # Opens and closes
  open_price = models.FloatField()
  open_date = models.CharField(max_length=25)
  close_price = models.FloatField()
  close_date = models.CharField(max_length=25)

  stoploss = models.FloatField()
  takeprofit = models.FloatField()

  profit = models.FloatField()

  symbol = models.CharField(max_length=20)

  ticket = models.PositiveIntegerField()
  type_operation = models.CharField(max_length=11)

  def __str__(self):
    """Return profit and type."""
    return f'{self.type_operation}: {self.profit}'
