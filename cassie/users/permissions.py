"""User permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cassie.users.models import User

class IsAccoutOwner(BasePermission):
  """Allow accesss only to objects owned by the requesting user."""

  def has_object_permission(self, request, view, obj):
    """Check obj and user are the same."""
    return obj == request.user

class IsAdminOrAccountOwner(BasePermission):
  """Allow access only to admin or owners of account."""

  def has_permission(self, request, view):
    return request.user.is_admin or view.user == request.user
