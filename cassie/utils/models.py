"""Django models utilities."""

# Django
from django.db import models

class CassieModel(models.Model):
  """Cassie base model.

    CassieModel acts as an abstarct base class from which every
    other model in the project will inherit. This class provides
    every tabla with the following attributes:
      + created (Datetime): store the datetime the object was created
      + modified (Datetime): store the last datetime the object was modified
  """

  created = models.DateTimeField(
    'created at',
    auto_now_add=True,
    help_text='Date time on which the object was created.'
  )

  modified = models.DateTimeField(
    'modified at',
    auto_now=True,
    help_text='Date time on which the object was last modified.'
  )

  class Meta:
    """Meta Class."""
    abstract = True
    
    get_latest_by = 'created'
    ordering = ['-created', '-modified']