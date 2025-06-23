import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from CestaMagica import settings
from Inventario.models import Producto
from pedido.models import Pedido
from django.views.decorators.http import require_POST
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.error.transbank_error import TransbankError
from django.http import FileResponse
from .models import DetallePedido, Pedido
from .utils import generar_pdf_pedido
import os
from django.conf import settings

@login_required
def confirmar_pedido(request):
    cart = request.session.get("cart", {})
    perfil = request.session.get('perfil')

    if not cart:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("productos")
    
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para confirmar tu pedido.")
        return redirect("login")

    total = 0
    for item in cart.values():
        total += item["price"] * item["quantity"]

    pedido = Pedido.objects.create(
        usuario=request.user,
        estado="PAG",
        total=total,
        metodo_pago="Webpay",
    )

    for item in cart.values():
        try:
            producto = Producto.objects.get(id=item["product_id"])
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item["quantity"],
                precio_unitario=item["price"],
            )
        except Producto.DoesNotExist:
            continue

    productos = [{
        "nombre": item["name"],
        "description": item["description"],
        "cantidad": item["quantity"],
        "precio": item["price"],
        "subtotal": item["price"] * item["quantity"],
        "imagen": item["image"]
    } for item in cart.values()]

    context = {
        "productos": productos,
        "total": total,
        "pedido": pedido,
        "pedido_id": str(pedido.id),
        "perfil": perfil,
    }
    return render(request, "CestaMagica/pedido_confirmacion.html", context)
def _tbk_options():
    return WebpayOptions(
        commerce_code=settings.WEBPAY_COMMERCE_CODE,
        api_key=settings.WEBPAY_API_KEY,
        integration_type=settings.WEBPAY_ENV 
    )


@login_required
@require_POST
def iniciar_pago(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id, usuario=request.user, estado="PEND")

    metodo = request.POST.get("metodo_retiro")
    notas = request.POST.get("notas")

    if metodo:
        pedido.metodo_retiro = metodo
    if notas:
        pedido.notas = notas
    pedido.save(update_fields=["metodo_retiro", "notas"])

    buy_order = str(pedido.codigo_pedido)
    session_id = str(request.user.id)
    amount = float(pedido.total)
    return_url = request.build_absolute_uri(reverse("pedido:webpay_retorno"))

    tx = Transaction(options=_tbk_options())

    try:
        resp = tx.create(buy_order, session_id, amount, return_url)
    except TransbankError as e:
        return JsonResponse({"error": f"Error en Transbank: {e}"}, status=500)

    pedido.token_ws = resp["token"]
    pedido.save(update_fields=["token_ws"])

    if request.GET.get("test") == "1":
        return JsonResponse({
            "url_pago": resp["url"] + "?token_ws=" + resp["token"],
            "token": resp["token"]
        })

    return redirect(resp["url"] + "?token_ws=" + resp["token"])



@login_required
def webpay_retorno(request):
    token = request.GET.get("token_ws")
    if not token:
        messages.error(request, "Token no entregado por Webpay.")
        return redirect("productos")

    tx  = Transaction(options=_tbk_options())
    resp = tx.commit(token)

    pedido = get_object_or_404(Pedido, token_ws=token)

    if resp["status"] == "AUTHORIZED":
        pedido.estado = "PAG"
        pedido.metodo_pago = "Webpay"
        pedido.save(update_fields=["estado", "metodo_pago"])
        return redirect("pedido:pedido_exito", pedido_id=pedido.id)

    pedido.estado = "CAN"
    pedido.save(update_fields=["estado"])
    messages.error(request, "Pago rechazado por Transbank.")
    return redirect("pedido:confirmar_pedido")

def descargar_pdf_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    items = pedido.items.all()

    pedido_data = {
        "codigo_pedido": pedido.codigo_pedido,
        "fecha": pedido.fecha.strftime("%d/%m/%Y"),
        "estado": pedido.get_estado_display(),
        "metodo_retiro": pedido.metodo_retiro,
        "metodo_pago": pedido.metodo_pago,
        "total": f"{pedido.total:,.0f}",
    }

    items_data = [{
        "producto": i.producto.nombre,
        "cantidad": i.cantidad,
        "precio_unitario": f"{i.precio_unitario:,.0f}",
        "subtotal": f"{i.subtotal:,.0f}",
    } for i in items]

    print([str(item) for item in items])

    logo_path = os.path.join(settings.BASE_DIR, "static", "logo.png")
    buffer = generar_pdf_pedido(pedido_data, items_data, logo_path)

    return FileResponse(buffer, as_attachment=True, filename=f"Pedido_{pedido.codigo_pedido}.pdf")

@login_required
def pedido_exito(request, pedido_id):
    perfil = request.session.get('perfil')
    pedido = get_object_or_404(Pedido, pk=pedido_id, usuario=request.user, estado="PAG")
    request.session["cart"] = {}

    context = {
        "pedido": pedido,
        "productos": pedido.items.all(),
        "perfil": perfil,
    }
    return render(request, "CestaMagica/pedido_exitoso.html", context)
