"""Main URLs module."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    # Apps
    path('', include(('cassie.users.urls', 'users'), namespace='users')),
    path('', include(('cassie.licenses.urls', 'licenses'), namespace='licenses')),
    path('', include(('cassie.accounts.urls', 'accounts'), namespace='accounts')),
    path('', include(('cassie.reports.urls', 'reports'), namespace='reports')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
