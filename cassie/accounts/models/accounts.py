"""Accounts models."""

# Django
from django.db import models

# Utilities
from cassie.utils.models import CassieModel

class Account(CassieModel):
  """Account model.
    An account object is a Trading account in MetaTrader4.
    Each account is associated with a license and 
    occupies an available space from this.
  """

  license = models.ForeignKey('licenses.License', on_delete=models.CASCADE)
  account_number = models.PositiveIntegerField()
  initial_value = models.FloatField()
  current_value = models.FloatField()
  is_active = models.BooleanField(default=True)

  def __str__(self):
    """Return license and account number."""
    return f'{self.license.key}: {self.account_number}'
