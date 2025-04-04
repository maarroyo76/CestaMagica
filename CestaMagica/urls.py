from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Rest_API import viewsLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Inventario.urls')),
    path('api/', include('Rest_API.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
