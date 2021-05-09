"""User Licenses views."""

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from cassie.users.permissions import IsAccoutOwner, IsAdminOrAccountOwner

# Serializers
# from cassie.users.serializers import UserModelSerializer
# from cassie.licenses.serializers import LicenseModelSerializer
from cassie.accounts.serializers import AccountModelSerializer

# Models
from cassie.users.models import User
from cassie.licenses.models import License
from cassie.accounts.models import Account

class UserAccountViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """Users Licenses View Set."""
  
  serializer_class = AccountModelSerializer
  queryset = Account.objects.all()
  permission_classes = [IsAuthenticated, IsAdminOrAccountOwner]

  def dispatch(self, request, *args, **kwargs):
    """Verify users exists."""
    username = kwargs['username']
    self.user = get_object_or_404(User, username=username)
    return super(UserAccountViewSet, self).dispatch(request, *args, **kwargs)

  def list(self, request, *args, **kwargs):
    """Licenses of user."""
    licenses = License.objects.filter(owner=self.user)
    accounts = Account.objects.filter(account_number=0)
    for license in licenses:
      accounts = accounts | Account.objects.filter(license=license)
    data = AccountModelSerializer(accounts, many=True).data
    return Response(data, status=status.HTTP_200_OK)

  def retrieve(self, request, *args, **kwargs):
    account = Account.objects.filter(
      account_number= kwargs['pk']
    )
    data = AccountModelSerializer(account, many=True).data
    return Response(data, status=status.HTTP_200_OK)

