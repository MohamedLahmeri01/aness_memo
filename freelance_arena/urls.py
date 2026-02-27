from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/auth/', include('accounts.urls', namespace='accounts')),
    path('api/competitions/', include('competitions.urls', namespace='competitions')),
    path('api/proposals/', include('proposals.urls', namespace='proposals')),
    path('api/feedback/', include('feedback.urls', namespace='feedback')),
    path('api/notifications/', include('notifications.urls', namespace='notifications')),
    path('api/payments/', include('payments.urls', namespace='payments')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
