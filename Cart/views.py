from django.shortcuts import redirect, render
from .cart import Cart
from Inventario.models import Producto

# Create your views here.

def add_to_cart(request, producto_id):
    cart = Cart(request)
    product = Producto.objects.get(id=producto_id)
    cart.add(product)
    return redirect('cart:cart_detail')

def remove_from_cart(request, producto_id):
    cart = Cart(request)
    product = Producto.objects.get(id=producto_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def decrement_in_cart(request, producto_id):
    cart = Cart(request)
    product = Producto.objects.get(id=producto_id)
    cart.decrement(product)
    return redirect('cart:cart_detail')

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    total = cart.get_total()
    context = {
        'cart': cart,
        'total': total,
    }
    return render(request, 'cart/cart_detail.html', context)