"""Licenses models."""

# Django
from django.db import models

# Utilities
from cassie.utils.models import CassieModel

# Managers
from cassie.licenses.managers import LicensesManager

class License(CassieModel):
  """License model.
    A license is a private key bought an user to
    active Cassie Bot in a specific number of
    accounts.
  """

  owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
  key = models.CharField(max_length=50, unique=True)
  available_spaces = models.IntegerField(default=1)
  created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_by')
  is_active = models.BooleanField(default=True)

  objects = LicensesManager()

  def __str__(self):
    """Return owner and license."""
    return f'{self.owner.username}: {self.key}'
