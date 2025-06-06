import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from CestaMagica import settings
from pedido.models import Pedido
from Inventario.models import Producto
from django.views.decorators.http import require_POST

from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.error.transbank_error import TransbankError

@login_required
def confirmar_pedido(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("productos")
    
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para confirmar tu pedido.")
        return redirect("login")

    productos = []
    total = 0
    for item in cart.values():
        total += item["price"] * item["quantity"]
        productos.append({
            "nombre": item["name"],
            "description": item["description"],
            "cantidad": item["quantity"],
            "precio": item["price"],
            "subtotal": item["price"] * item["quantity"],
            "imagen": item["image"]
        })

    pedido = Pedido.objects.create(
        usuario=request.user,
        estado="PEND",
        total = total,
        metodo_pago="Webpay",
    )

    context = {
        "productos": productos,
        "total": total,
        "pedido": pedido,
        "pedido_id": str(pedido.id),
        
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

    try:
        datos = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    monto_str = datos.get("monto")
    if monto_str is None:
        return JsonResponse({"error": "Monto no proporcionado"}, status=400)

    # Validación simple: compara monto recibido con pedido.total usando float()
    try:
        if float(monto_str) != float(pedido.total):
            return JsonResponse({"error": "Monto inválido"}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Monto inválido"}, status=400)

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

    # Para test, responde con JSON y no redirige
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


@login_required
def pedido_exito(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id, usuario=request.user, estado="PAG")
    request.session["cart"] = {}

    context = {
        "pedido": pedido,
        "productos": pedido.items.all(),
    }
    return render(request, "CestaMagica/pedido_exitoso.html", context)
