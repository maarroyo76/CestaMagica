from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'productos', views.ProductoViewSet, basename='producto')
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')
router.register(r'marcas', views.MarcaViewSet, basename='marca')

urlpatterns = [
    path('', include(router.urls)),
]