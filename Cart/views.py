from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .cart import Cart
from Inventario.models import Producto

def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def get_cart_state(request):
    cart = Cart(request)
    cart_items = []
    total = 0
    total_items = 0

    for item in cart:
        subtotal = item["price"] * item["quantity"]
        total += subtotal
        total_items += item["quantity"]
        cart_items.append({
            "product_id": item["product_id"],
            "name": item["name"],
            "description": item["description"],
            "image": item["image"],
            "price": item["price"],
            "quantity": item["quantity"],
            "subtotal": subtotal,
        })

    return JsonResponse({
        "cart_items": cart_items,
        "total": total,
        "total_items": total_items
    })

@require_POST
def add_to_cart(request, producto_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=producto_id)
    quantity = int(request.POST.get('cantidad', 1))
    cart.add(product, quantity)

    if is_ajax(request):
        items = []
        for item in cart.cart.values():
            subtotal = item['price'] * item['quantity']
            items.append({
                'product_id': item['product_id'],
                'name': item['name'],
                'image': item['image'],
                'price': int(item['price']),
                'quantity': item['quantity'],
                'description': item['description'],
                'subtotal': int(subtotal),
            })
            total_items = sum(item['quantity'] for item in items)
        return JsonResponse({
            'message': 'Producto agregado',
            'cart_items': items,
            'total': int(cart.get_total()),
            'total_items': total_items,
        })
    return redirect('cart:cart_detail')



@require_POST
def remove_from_cart(request, producto_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=producto_id)
    cart.remove(product)

    if is_ajax(request):
        items = []
        for item in cart.cart.values():
            subtotal = item['price'] * item['quantity']
            items.append({
                'product_id': item['product_id'],
                'name': item['name'],
                'image': item['image'],
                'price': int(item['price']),
                'quantity': item['quantity'],
                'description': item['description'],
                'subtotal': int(subtotal),
            })
        total_items = sum(item['quantity'] for item in items)
        return JsonResponse({
            'message': 'Producto eliminado',
            'cart_items': items,
            'total': int(cart.get_total()),
            'total_items': total_items,
        })
    return redirect('cart:cart_detail')



@require_POST
def decrement_in_cart(request, producto_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=producto_id)
    cart.decrement(product)

    if is_ajax(request):
        items = []
        for item in cart.cart.values():
            subtotal = item['price'] * item['quantity']
            items.append({
                'product_id': item['product_id'],
                'name': item['name'],
                'image': item['image'],
                'price': int(item['price']),
                'quantity': item['quantity'],
                'description': item['description'],
                'subtotal': int(subtotal),
            })
        total_items = sum(item['quantity'] for item in items)

        return JsonResponse({
            'message': 'Cantidad decrementada',
            'cart_items': items,
            'total': int(cart.get_total()),
            'total_items': total_items,
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
    perfil = request.session.get('perfil')

    return render(request, 'CestaMagica/carrito.html', {
        'cart': cart,
        'total': cart.get_total(),
        'perfil': perfil,
    })


@require_POST
def update_quantity(request, producto_id):
    action = request.POST.get("action")
    cart = Cart(request)
    product = get_object_or_404(Producto, id=producto_id)

    if action == "add":
        cart.add(product)
    elif action == "remove":
        cart.decrement(product)
    else:
        return JsonResponse({"error": "Acción inválida"}, status=400)

    quantity = cart.cart.get(str(producto_id), {}).get("quantity", 0)

    total_items = sum(item["quantity"] for item in cart.cart.values())
    total_price = cart.get_total()

    return JsonResponse({
        "quantity": quantity,
        "total_items": total_items,
        "total_price": f"{total_price:,.2f}"
    })
