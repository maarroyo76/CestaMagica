from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .cart import Cart
from Inventario.models import Producto

def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

@require_POST
def add_to_cart(request, producto_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=producto_id)
    cart.add(product)

    if is_ajax(request):
        return JsonResponse({
            'message': 'Producto agregado',
            'cart_items': list(cart.cart.values()),
            'total': cart.get_total(),
        })
    return redirect('cart:cart_detail')


@require_POST
def remove_from_cart(request, producto_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=producto_id)
    cart.remove(product)

    if is_ajax(request):
        return JsonResponse({
            'message': 'Producto eliminado',
            'cart_items': list(cart.cart.values()),
            'total': cart.get_total(),
        })
    return redirect('cart:cart_detail')


@require_POST
def decrement_in_cart(request, producto_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=producto_id)
    cart.decrement(product)

    if is_ajax(request):
        return JsonResponse({
            'message': 'Cantidad decrementada',
            'cart_items': list(cart.cart.values()),
            'total': cart.get_total(),
        })
    return redirect('cart:cart_detail')


@require_POST
def clear_cart(request):
    cart = Cart(request)
    cart.clear()

    if is_ajax(request):
        return JsonResponse({
            'message': 'Carrito vaciado',
            'cart_items': [],
            'total': cart.get_total(),
        })
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'CestaMagica/carrito.html', {
        'cart': cart,
        'total': cart.get_total(),
    })
