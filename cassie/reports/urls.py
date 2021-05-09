"""Reports URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import reports as reports_views

router = DefaultRouter()
router.register(r'reports', reports_views.ReportsViewSet, basename='reports')
router.register(r'reports/bot', reports_views.CreateReportViewSet, basename='botReports')

urlpatterns = [
  path('', include(router.urls))
]
