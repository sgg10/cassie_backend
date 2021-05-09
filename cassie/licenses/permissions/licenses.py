"""Licenses permissions classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cassie.users.models import User
from cassie.licenses.models import License

class IsAdminUser(BasePermission):
  """Allow access only admin users."""

  message = 'Only admin users have permission to this action.'

  def has_permission(self, request, view):
    """Verify user have an admin status."""
    try:
      User.objects.get(
        username=request.user.username,
        email=request.user.email,
        is_admin=True,
        is_verified=True
      )
    except User.DoesNotExist:
      return False
    return True

class IsLicenceOwnerOrUserAdmin(BasePermission):
  """Allow access only admin user or license owner"""
  
  def has_permission(self, request, view):
    try:
      User.objects.get(
        username=request.user.username,
        is_admin=True,
        is_verified=True
      )
    except User.DoesNotExist:
      try:
        License.objects.get(
          key=view.kwargs['key'],
          owner=request.user
        )
      except License.DoesNotExist:
        return False
    return True