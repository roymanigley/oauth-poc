from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from django.http import JsonResponse
from rest_framework import status


def not_found_view(request, *args, **kwargs):
    return JsonResponse(data={'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r"^oauth/applications/.*$", not_found_view),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('api/', include('apps.tenant.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'
         ),
    path('', RedirectView.as_view(url='/api/schema/redoc/'))
]
