"""Licences views."""

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
# from rest_framework.exceptions import MethodNotAllowed

# Models
from cassie.licenses.models import License
from cassie.users.models import User

# Serializers
from cassie.licenses.serializers import CreateLicenseSerializer, LicenseModelSerializer
from cassie.users.serializers import UserModelSerializer

# Permissions
from cassie.licenses.permissions import IsAdminUser, IsLicenceOwnerOrUserAdmin
from rest_framework.permissions import IsAuthenticated

class LicenseViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
  """License view set."""

  serializer_class = LicenseModelSerializer
  lookup_field = 'key'

  def get_queryset(self):
    """Return licenses."""
    return License.objects.all()

  def get_permissions(self):
    """Assing permissions based on action."""
    permissions = [IsAuthenticated]
    if self.action in ['create', 'update', 'list', 'partial_update', 'destroy']:
      permissions.append(IsAdminUser)
    if self.action == 'retrieve':
      permissions.append(IsLicenceOwnerOrUserAdmin)
    return [permission() for permission in permissions]

  def get_serializer_class(self):
    if self.action == 'create':
      return CreateLicenseSerializer
    return LicenseModelSerializer

  def create(self, request):
    context = self.get_serializer_context()
    context['owner'] = request.data['owner']
    context['created_by'] = request.user
    serializer_class = self.get_serializer_class()
    serializer = serializer_class(
      data=request.data,
      context=context
    )
    serializer.is_valid(raise_exception=True)
    license = serializer.save()
    data = LicenseModelSerializer(license).data
    return Response(data, status=status.HTTP_201_CREATED)

  def perform_destroy(self, instance):
    """Disable License."""
    instance.is_active = False
    instance.save()