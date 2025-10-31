from django.urls import path
from . import views

app_name = "pedido"

urlpatterns = [
    path('confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
    path("pagar/<uuid:pedido_id>/", views.iniciar_pago, name="iniciar_pago"),
    path("retorno/", views.webpay_retorno, name="webpay_retorno"),
    path("exito/<uuid:pedido_id>/", views.pedido_exito, name="pedido_exito"),
     path("descargar_pdf/<uuid:pedido_id>/", views.descargar_pdf_pedido, name="descargar_pdf_pedido"),
]