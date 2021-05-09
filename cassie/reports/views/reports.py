"""Reports views."""

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Serializers
from cassie.reports.serializers import (
  ReportModelSerializer,
  CreateReportSerializer
)

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from cassie.reports.permissions import IsAccountOwnerOrAdminUser

# Models
from cassie.reports.models import Report
from cassie.accounts.models import Account

class CreateReportViewSet(viewsets.GenericViewSet):
  """Create Report viewset.
    Handle creation a report for an account.
  """

  permission_classes = [AllowAny]

  @action(detail=False, methods=['POST'])
  def send(self, request):
    """Create report."""
    serializer = CreateReportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    data = { 'message': 'Report sended success' }
    return Response(data, status=status.HTTP_201_CREATED)

class ReportsViewSet(mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
  """Report view set.
    Handle list and retrieve reports only owners or
    admin users.
  """

  queryset = Report.objects.all()
  lookup_url_kwarg = 'account'
  serializer_class = ReportModelSerializer
  permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminUser]
  
  def retrieve(self, request, *args, **kwargs):
    try:
      queryset = Report.objects.filter(
        account=Account.objects.get(
          account_number=kwargs['account']
        )
      )
      data = ReportModelSerializer(queryset, many=True).data
    except:
      return Response({ 'detail': 'Not found' }, status=status.HTTP_404_NOT_FOUND)
    return Response(data, status=status.HTTP_200_OK)
