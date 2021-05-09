"""Accounts permission classes."""

# Django REST Framwork
from rest_framework.permissions import BasePermission

# Models
from cassie.licenses.models import License
from cassie.accounts.models import Account

class IsOwnerOfLicenseOrAdmin(BasePermission):
  """Alllow access only owner or admin user."""

  def has_permission(self, request, view):
    try:
      account = Account.objects.get(
        account_number=view.kwargs['account_number']
      )
      license = License.objects.get(
        owner=account.license.owner,
        key=account.license.key
      )
      if license.owner != request.user:
        return False
    except Account.DoesNotExist:
      if request.user.is_admin:
        return True
      return False
    except KeyError:
      return False
    return True

class IsOwnerOfLicense(BasePermission):
  """Alllow access only owner or admin user."""

  def has_permission(self, request, view):
    try:
      License.objects.get(
        owner=request.user,
        key=request.data['license']
      )
    except License.DoesNotExist:
      return False
    except KeyError:
      return False
    return True
