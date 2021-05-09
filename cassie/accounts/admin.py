"""Account admin."""

# Django
from django.contrib import admin

# Models
from cassie.accounts.models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
  """Account admin."""
  list_display = (
    'account_number',
    'license',
    'initial_value',
    'current_value',
    'is_active'
  )
  search_fields = (
    'account_number',
    'license'
  )
  list_filter = ('is_active',)