"""Accounts serializer."""

# Django REST Framwork
from rest_framework import serializers

# Models
from cassie.accounts.models import Account
from cassie.licenses.models import License

# Serializer
from cassie.licenses.serializers import LicenseModelSerializer

class AccountModelSerializer(serializers.ModelSerializer):
  """Account model serializer."""

  license = LicenseModelSerializer(read_only=True)
  account_number = serializers.IntegerField()
  initial_value = serializers.FloatField()
  current_value = serializers.FloatField()

  class Meta:
    """Meta class."""

    model = Account
    fields = (
      'license',
      'account_number',
      'initial_value',
      'current_value',
      'is_active'
    )

    read_only_fields = (
      'license',
      'account_number',
      'initial_value',
      'is_active'
    )

class CreateAccountSerializer(serializers.Serializer):
  """Create Account serializer.

    Handle the creation of a new account by user.
  """
  account_number = serializers.IntegerField()
  initial_value = serializers.FloatField()

  def validate(self, data):
    """Validate Licenses exist, has available spaces
      and the accout doesn't exists."""
    try:
      self.context['license'] = License.objects.get(
        key=self.context['license'],
        owner=self.context['owner'],
      )
    except License.DoesNotExist:
      raise serializers.ValidationError('The license does not exists.')

    if not self.context['license'].is_active:
      raise serializers.ValidationError('The license does not active.')

    try:
      Account.objects.get(
        license=self.context['license'],
        account_number=data['account_number']
      )
      raise serializers.ValidationError('The account already exists.')
    except Account.DoesNotExist:
      pass
    
    if self.context['license'].available_spaces < 1:
      raise serializers.ValidationError('The license have not available spaces.')

    return data

  def create(self, data):
    """Create account."""
    account = Account.objects.create(
      license=self.context['license'],
      account_number=data['account_number'],
      initial_value=data['initial_value'],
      current_value=data['initial_value'],
      is_active=True
    )
    self.context['license'].available_spaces -= 1
    self.context['license'].save()

    return account

class AuthorizationAccountSerializer(serializers.Serializer):
  """ Authorization Account Serializer."""

  account_number = serializers.IntegerField() 

  def validate(self, data):
    """Validate if account is registred and active."""
    try:
      self.context['license'] = License.objects.get(
        key=self.context['license'],
      )
    except License.DoesNotExist:
      raise serializers.ValidationError('The license does not exists.')

    if not self.context['license'].is_active:
      raise serializers.ValidationError('The license does not active.')

    try:
      self.context['account'] = Account.objects.get(
        license=self.context['license'],
        account_number=data['account_number']
      )
    except Account.DoesNotExist:
      raise serializers.ValidationError('The account does not exists.')

    if not self.context['account'].is_active:
      raise serializers.ValidationError('The account does not active.')
    
    return data