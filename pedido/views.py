from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from CestaMagica import settings
from Inventario.models import Producto
from pedido.models import Pedido, DetallePedido
from django.views.decorators.http import require_POST
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.error.transbank_error import TransbankError
from .utils import generar_pdf_pedido
import os
from django.conf import settings
from django.db import transaction

@login_required
@transaction.atomic
def confirmar_pedido(request):
    cart = request.session.get("cart", {})
    perfil = request.session.get('perfil')

    if not cart:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("productos")
    
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para confirmar tu pedido.")
        return redirect("iniciar_sesion")

    total = 0
    items_para_procesar = []
    
    for item_key, item in cart.items():
        try:
            producto = Producto.objects.select_for_update().get(id=item["product_id"])

            if not producto.is_available:
                messages.error(request, f"Lo sentimos, '{producto.nombre}' se encuentra sin stock.")
                return redirect("cart:cart_detail")

            if producto.stock_vendible < item["quantity"]:
                messages.error(request, f"Lo sentimos, no hay suficiente stock para '{producto.nombre}'. Quedan {producto.stock_vendible} unidades disponibles.")
                return redirect("cart:cart_detail")
            
            item_subtotal = producto.precio * item["quantity"]
            total += item_subtotal
            
            items_para_procesar.append({
                "producto_obj": producto,
                "cantidad": item["quantity"],
                "precio_unitario": producto.precio,
                "subtotal": item_subtotal,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "imagen": producto.imagen.url
            })

        except Producto.DoesNotExist:
            messages.error(request, f"Un producto en tu carrito ya no existe y fue eliminado.")
            cart.pop(item_key, None)
            request.session.modified = True
            return redirect("cart:cart_detail")
        
    pedido = Pedido.objects.create(
        usuario=request.user,
        estado="PEND", 
        total=total,
        metodo_pago="Webpay (Pendiente)"
    )

    for item in items_para_procesar:
        producto = item["producto_obj"]
        
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item["cantidad"],
            precio_unitario=item["precio_unitario"],
        )
        
        producto.stock -= item["cantidad"]
        producto.save(update_fields=["stock"])

    context = {
        "productos": items_para_procesar,
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
        try:
            with transaction.atomic():
                for item in pedido.items.all():
                    item.producto.stock += item.cantidad
                    item.producto.save(update_fields=["stock"])
                pedido.estado = "CAN"
                pedido.save(update_fields=["estado"])
            messages.error(request, "Error al iniciar el pago. Tu pedido ha sido cancelado y el stock restablecido.")
            return redirect("cart:cart_detail")
        except Exception as e_rollback:
            messages.error(request, f"Error CRÍTICO. Contacta a soporte. Pedido: {pedido.codigo_pedido}")
            return redirect("cart:cart_detail")
            
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
        messages.error(request, "Pago cancelado.")
        
        try:
            pedido = Pedido.objects.get(token_ws=token, usuario=request.user, estado="PEND")
            with transaction.atomic():
                for item in pedido.items.all():
                    item.producto.stock += item.cantidad
                    item.producto.save(update_fields=["stock"])
                pedido.estado = "CAN"
                pedido.save(update_fields=["estado"])
            messages.info(request, "Tu pedido ha sido cancelado y el stock ha sido restablecido.")
        except Pedido.DoesNotExist:
            pass
            
        return redirect("cart:cart_detail")

    tx  = Transaction(options=_tbk_options())
    
    try:
        resp = tx.commit(token)
    except TransbankError as e:
        messages.error(request, f"Error de Transbank: {e.message}")
        return redirect("cart:cart_detail")

    pedido = get_object_or_404(Pedido, token_ws=token, usuario=request.user)

    if resp["status"] == "AUTHORIZED":
        pedido.estado = "PAG"
        pedido.metodo_pago = "Webpay"
        pedido.save(update_fields=["estado", "metodo_pago"])
        
        return redirect("pedido:pedido_exito", pedido_id=pedido.id)

    pedido.estado = "CAN"
    pedido.save(update_fields=["estado"])

    try:
        with transaction.atomic():
            for item in pedido.items.all():
                item.producto.stock += item.cantidad
                item.producto.save(update_fields=["stock"])
        messages.error(request, "Pago rechazado por Transbank. Tu pedido fue cancelado y el stock restablecido.")
    except Exception as e:
        messages.error(request, f"Pago rechazado. Error CRÍTICO al re-abastecer stock. Contacta a soporte. Pedido: {pedido.codigo_pedido}")

    return redirect("cart:cart_detail")


def descargar_pdf_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    perfil = request.session.get('perfil') 
    
    if pedido.usuario != request.user and perfil not in ['admin', 'staff']:
        messages.error(request, "No tienes permiso para ver este pedido.")
        return redirect("home")
    
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

    logo_path = os.path.join(settings.BASE_DIR, "static", "Logo.png")
    buffer = generar_pdf_pedido(pedido_data, items_data, logo_path)

    return FileResponse(buffer, as_attachment=True, filename=f"Pedido_{pedido.codigo_pedido}.pdf")


@login_required
def pedido_exito(request, pedido_id):
    perfil = request.session.get('perfil')
    pedido = get_object_or_404(Pedido, pk=pedido_id, usuario=request.user, estado="PAG")

    request.session["cart"] = {}
    request.session.modified = True

    context = {
        "pedido": pedido,
        "productos": pedido.items.all(),
        "perfil": perfil,
    }
    return render(request, "CestaMagica/pedido_exitoso.html", context)
