"""Reports models."""

# Django 
from django.db import models

# Utilities
from cassie.utils.models import CassieModel

class Report(CassieModel):
  """Report model.
    Report obj is a daily report after ends
    all operative day.
  """

  account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)

  balance = models.FloatField()
  equity = models.FloatField()
  total_profit = models.FloatField()

  date = models.DateTimeField(auto_now_add=True)

  trades = models.ManyToManyField('trades.Trade', blank=True)

  def __str__(self):
    """Return date and account number"""
    return f'{self.account.account_number}: {self.date}'
