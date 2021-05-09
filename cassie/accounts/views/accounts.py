"""Accounts views."""

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Models
from cassie.licenses.models import License
from cassie.accounts.models import Account

# Serializers
from cassie.accounts.serializers import (
  AccountModelSerializer,
  CreateAccountSerializer,
  AuthorizationAccountSerializer
)
from cassie.licenses.serializers import LicenseModelSerializer

# Permissions
from cassie.accounts.permissions import (
  IsOwnerOfLicense,
  IsOwnerOfLicenseOrAdmin
)
from cassie.licenses.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated, AllowAny

class AccountViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
  """Account View Set."""

  queryset = Account.objects.all()
  lookup_field = 'account_number'

  def get_serializer_class(self):
    if self.action == 'create':
      return CreateAccountSerializer
    return AccountModelSerializer

  def get_permissions(self):
    """Assing permissions based on action."""
    permissions = [IsAuthenticated]
    if self.action == 'create':
      permissions.append(IsOwnerOfLicense)
    elif self.action in ['retrieve', 'update', 'partial_update']:
      permissions.append(IsOwnerOfLicenseOrAdmin)
    elif self.action == 'list':
      permissions.append(IsAdminUser)
    return [permission() for permission in permissions]

  def create(self, request):
    context = self.get_serializer_context()
    context['license'] = request.data['license']
    context['owner'] = request.user
    serializer_class = self.get_serializer_class()
    serializer = serializer_class(
      data=request.data,
      context=context
    )
    serializer.is_valid(raise_exception=True)
    data = AccountModelSerializer(serializer.save()).data
    return Response(data, status=status.HTTP_201_CREATED)

  def perform_destroy(self, instance):
    """Disable Account."""
    if instance.is_active:
      instance.is_active = False
      license = instance.license
      license.available_spaces += 1
      license.save()
      instance.save()

class AccountAuthorizationViewset(viewsets.GenericViewSet):
  """Account Authorization viewset.
    Handle operation an account if is valid account.
  """
  permission_classes = [AllowAny]

  @action(detail=False, methods=['POST'])
  def verify(self, request):
    """Allow use Cassie bot if an account is valid."""
    context = self.get_serializer_context()
    context['license'] = request.data['license']
    serializer = AuthorizationAccountSerializer(
      data=request.data,
      context=context
    )
    serializer.is_valid(raise_exception=True)
    return Response({ 'permission': True }, status=status.HTTP_200_OK)
