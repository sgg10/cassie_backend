"""Report permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cassie.accounts.models import Account

class IsAccountOwnerOrAdminUser(BasePermission):
  """Allow access only account owner or any admin user."""

  def has_permission(self, request, view):
    """Verify account or admin status."""
    try:
      account = Account.objects.get(
        account_number=view.kwargs['account']
      )

      if request.user.is_admin:
        return True
      elif account.license.owner == request.user:
        return True
      return False
    except Account.DoesNotExist:
      return False
