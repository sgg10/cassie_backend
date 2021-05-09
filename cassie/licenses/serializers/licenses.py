"""Licenses serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from cassie.users.models import User
from cassie.licenses.models import License

# Serializer
from cassie.users.serializers import UserModelSerializer

class LicenseModelSerializer(serializers.ModelSerializer):
  """License model serializer."""

  owner = UserModelSerializer(read_only=True)
  key = serializers.CharField(min_length=20, max_length=50, required=False)
  available_spaces = serializers.IntegerField(default=1)
  created_by = UserModelSerializer(read_only=True)

  class Meta:
    """Meta class."""

    model = License
    fields = (
      'owner',
      'key',
      'available_spaces',
      'created_by'
    )

    read_only_fields = (
      'owner',
      'key',
      'created_by'
    )

class CreateLicenseSerializer(serializers.Serializer):
  """Create license serializer.

    Handle the creation of a new license by admin user to 
    another user.
  """
  available_spaces = serializers.IntegerField(default=1)

  def validate(self, data):
    """Validate owner user exists."""
    try:
      self.context['owner'] = User.objects.get(
        username=self.context['owner'],
        is_verified=True
      )
    except User.DoesNotExist:
      raise serializers.ValidationError('Invalid or not exists owner user.')
    return data

  def create(self, data):
    """Create License."""
    license = License.objects.create(
      owner=self.context['owner'],
      available_spaces=data['available_spaces'],
      created_by=self.context['created_by']
    )
    return license
