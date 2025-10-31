from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Rest_API import viewsLogin

from Inventario.views import error_400_view, error_403_view, error_404_view, error_500_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Inventario.urls')),
    path('api/', include('Rest_API.urls')),
]

if hasattr(settings, 'MEDIA_URL') and hasattr(settings, 'MEDIA_ROOT'):
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    else:
        from django.views.static import serve
        urlpatterns += [
            path(f'{settings.MEDIA_URL.lstrip("/")}<path:path>',
                 serve, {'document_root': settings.MEDIA_ROOT}),
        ]

handler404 = error_404_view
handler500 = error_500_view
handler403 = error_403_view
handler400 = error_400_view
