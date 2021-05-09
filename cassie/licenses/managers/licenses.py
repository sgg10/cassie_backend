"""Licenses managers."""

# Django
from django.db import models

# Utils
import random
from string import digits

class LicensesManager(models.Manager):
  """Licenses creations.
    Use to handle code creation.
  """

  CODE_LENGTH = 16
  LICENSE_PREFIX = 'SGG-'

  def create(self, **kwargs):
    """Handle license creation."""
    code = ''.join(random.choices(digits, k=self.CODE_LENGTH))
    key = self.LICENSE_PREFIX + code
    while self.filter(key=key).exists():
      code = ''.join(random.choices(digits, k=self.CODE_LENGTH))
      key = self.LICENSE_PREFIX + code
    kwargs['key'] = key
    return super(LicensesManager, self).create(**kwargs)