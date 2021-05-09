"""Report model admin."""

# Django
from django.contrib import admin

# Models
from cassie.reports.models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
  """Report admin."""
  list_display = (
    'account',
    'balance',
    'total_profit',
    'date'
  )
  search_fields = (
    'account',
    'balance',
    'total_profit'
  )
