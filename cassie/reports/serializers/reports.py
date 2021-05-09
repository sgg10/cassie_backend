"""Reports serializer."""

# Django REST Framework
from rest_framework import serializers

# Models 
from cassie.reports.models import Report
from cassie.trades.models import Trade
from cassie.accounts.models import Account
from cassie.licenses.models import License
from cassie.users.models import User

# Serializers
from cassie.trades.serializers import TradeModelSerializer
from cassie.accounts.serializers import AccountModelSerializer

class ReportModelSerializer(serializers.ModelSerializer):
  """Report model serializer."""

  account = AccountModelSerializer(read_only=True)
  balance = serializers.FloatField()
  equity = serializers.FloatField()
  total_profit = serializers.FloatField()
  trades = TradeModelSerializer(read_only=True, many=True)

  class Meta:
    """Meta class."""
    model = Report
    fields = (
      'account',
      'balance',
      'equity',
      'total_profit',
      'trades',
      'date'
    )

class CreateReportSerializer(serializers.Serializer):
  """Create report serializer."""

  balance = serializers.FloatField()
  equity = serializers.FloatField()
  owner = serializers.CharField(max_length=50)
  account = serializers.IntegerField()
  license = serializers.CharField(max_length=50)
  trades = serializers.ListField()

  def validate(self, data):
    """Validate Account exists and organize 
      rest of data."""
    try:
      self.context['account'] = Account.objects.get(
        account_number=data['account'],
        license=License.objects.get(
          key=data['license'],
          owner=User.objects.get(username=data['owner'])
        )
      )
    except Account.DoesNotExist:
      raise serializers.ValidationError('The account does not exists.')
    except License.DoesNotExist:
      raise serializers.ValidationError('The license does not exists.')
    return data

  def create(self, data):
    """Create Report."""
    report = Report.objects.create(
      account=self.context['account'],
      balance=data['balance'],
      equity=data['equity'],
      total_profit=0
    )

    for trade in data['trades']:
      trade = Trade.objects.create(**trade)
      report.total_profit += trade.profit
      report.trades.add(trade)
    report.save()

    self.context['account'].current_value = report.balance
    self.context['account'].save()

    return report
