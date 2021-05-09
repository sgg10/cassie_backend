"""License admin."""

# Django
from django.contrib import admin

# Models
from cassie.licenses.models import License

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
  """License admin."""
  list_display = (
    'key',
    'owner',
    'available_spaces',
    'created_by',
    'is_active'
  )
  search_fields = (
    'key', 
    'owner__username', 
    'owner__first_name', 
    'owner__last_name',
    'created_by__username', 
    'created_by__first_name', 
    'created_by__last_name',
  ),
  list_filter = ('is_active',)
