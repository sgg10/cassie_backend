"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Models
from cassie.users.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
  list_display = (
    'username',
    'email',
    'first_name',
    'last_name',
    'is_active',
    'is_admin',
    'is_verified',
    'is_staff'
  )
  search_fields = ('email', 'username', 'first_name', 'last_name')
  list_filter = ('created', 'modified', 'is_admin', 'is_verified')