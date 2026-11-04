from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('django-admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('scholarships/', include('scholarships.urls', namespace='scholarships')),
    path('applications/', include('applications.urls', namespace='applications')),
    path('admin-panel/', include('administrator.urls', namespace='administrator')),
    path('dashboard/', include('accounts.dashboard_urls', namespace='dashboard')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler403 = 'accounts.views.custom_403'
handler404 = 'accounts.views.custom_404'
