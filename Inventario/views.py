from django.shortcuts import get_object_or_404, redirect, render
from .models import Producto, Categoria, Marca, userProfile
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .decorators import role_required
from django.db import transaction
from pedido.models import Pedido, DetallePedido

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    productos_destacados = Producto.objects.filter(destacado=True)[:8]
    perfil = request.session.get('perfil')
    context = {
        'perfil': perfil,
        'productos_destacados': productos_destacados
    }
    return render(request, 'CestaMagica/home.html', context)

def productos(request):
    perfil = request.session.get('perfil')
    productos = Producto.objects.all()
    categorias = Categoria.objects.all().order_by('nombre')
    marcas = Marca.objects.all().order_by('nombre')

    search_query = request.GET.get('search', '')
    marca = request.GET.get('marca', '')
    categoria_id = request.GET.get('categoria', '')
    orden = request.GET.get('orden', 'nombre')

    # Filtrar productos
    if search_query:
        productos = productos.filter(nombre__icontains=search_query)
    if marca:
        productos = productos.filter(marca__nombre__icontains=marca)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # Ordenar productos
    if orden == 'nombre_desc':
        productos = productos.order_by('-nombre')
    elif orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    else:
        productos = productos.order_by('nombre')

    paginator = Paginator(productos, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'perfil': perfil,
        'productos': page_obj,
        'categorias': categorias,
        'selected_categoria': categoria_id,
        'marcas': marcas,
        'selected_marca': marca,
        'search_query': search_query,
        'marca': marca,
        'categoria_id': categoria_id,
        'orden': orden,
        'page_obj': page_obj,
    }

    return render(request, 'CestaMagica/productos.html', context)

def retroceder(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@role_required('admin', 'staff')
def gestion(request):
    perfil = request.session.get('perfil')
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    categorias = categorias.order_by('nombre')
    marcas = Marca.objects.all()
    marcas = marcas.order_by('nombre')
    
    search_query = request.GET.get('search', '')
    marca_id = request.GET.get('marca', '')
    categoria_id = request.GET.get('categoria', '')

    if search_query:
        productos = productos.filter(nombre__icontains=search_query)

    if marca_id:
        productos = productos.filter(marca_id=marca_id)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    
    context = {
        'perfil': perfil,
        'productos': productos,
        'categorias': categorias,
        'marcas': marcas
    }

    return render(request, 'CestaMagica/Gestion/gestion.html', context)

def contacto(request):
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        print(nombre, email, mensaje)

        messages.success(request, 'Mensaje enviado correctamente')
        return redirect('contacto')
    
    perfil = request.session.get('perfil')
    context = {
        'perfil': perfil,
    }
    return render(request, 'CestaMagica/contacto.html', context)

@role_required('admin', 'staff')
def agregar_producto(request):
    perfil = request.session.get('perfil')
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)

        marca_id = request.POST.get('marca')
        marca = get_object_or_404(Marca, id=marca_id)

        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        stock = request.POST.get('stock')
        precio = request.POST.get('precio')
        imagen = request.FILES.get('imagen')
        isDestacado = request.POST.get('isDestacado') == 'on'

        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            stock=stock,
            precio=precio,
            categoria=categoria,
            marca=marca,
            destacado=isDestacado
        )
        if imagen:
            producto.imagen = imagen
        producto.save()

        messages.success(request, 'Producto agregado correctamente')
        return redirect('gestion')

    categorias = Categoria.objects.all()
    categorias = categorias.order_by('nombre')
    marcas = Marca.objects.all()
    marcas = marcas.order_by('nombre')

    context = {
        'perfil': perfil,
        'categorias': categorias,
        'marcas': marcas
    }

    return render(request, 'CestaMagica/Gestion/agregar.html', context)

@role_required('admin', 'staff')
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    perfil = request.session.get('perfil')

    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)

        marca_id = request.POST.get('marca')
        marca = get_object_or_404(Marca, id=marca_id)

        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion', '')
        producto.stock = request.POST.get('stock')
        producto.precio = request.POST.get('precio')
        producto.categoria = categoria
        producto.marca = marca
        if request.FILES.get('imagen'):
            producto.imagen = request.FILES.get('imagen')
        producto.save()

        messages.success(request, 'Producto editado correctamente')
        return redirect('gestion')

    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()

    context = {
        'perfil': perfil,
        'producto': producto,
        'categorias': categorias,
        'marcas': marcas
    }

    return render(request, 'CestaMagica/Gestion/editar.html', context)

@role_required('admin', 'staff')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()

    messages.success(request, 'Producto eliminado correctamente')
    return redirect('gestion')


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    perfil = request.session.get('perfil')

    context = {
        'producto': producto,
        'perfil': perfil
    }

    return render(request, 'CestaMagica/detalle.html', context)


def registro(request):
    if request.method == "POST":
        username = request.POST.get("user")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        password = request.POST.get("pass")
        confirm_pass = request.POST.get("confirm_pass")

        if password != confirm_pass:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "registro.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return render(request, "registro.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
            return render(request, "registro.html")
        
        telefono = '+56 9 ' + telefono.strip()
        
        newUser = User.objects.create_user(
            username=username,
            first_name=nombre,
            last_name=apellido,
            email=email,
            password=password
        )
        user_profile = userProfile(
            user=newUser,
            telefono=telefono,
            role='cliente',
        )
        user_profile.save()

        user = authenticate(request, usuario=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        
    return render(request, 'CestaMagica/auth/registro.html')

def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        clave = request.POST.get('pass')

        user = authenticate(request, username=username, password=clave)

        if user is not None:
            profile = userProfile.objects.get(user=user)
            request.session['perfil'] = profile.role

            login(request, user)
            if profile.role == 'admin' or profile.role == 'staff':
                return redirect('gestion')
            else:
                return redirect('home')
        else:
            return render(request, 'CestaMagica/auth/inicio_sesion.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'CestaMagica/auth/inicio_sesion.html')

@role_required('admin', 'staff', 'cliente')
def cerrar_sesion(request):
    logout(request)
    return redirect('home')


@role_required('admin', 'staff', 'cliente')
def perfil(request):
    user = request.user

    try:
        profile = userProfile.objects.get(user=user)
    except userProfile.DoesNotExist:
        profile = None

    perfil_session = request.session.get('perfil')

    context = {
        'user': user,
        'perfil': perfil_session,
        'profile': profile
    }
    return render(request, 'CestaMagica/perfil.html', context)


@role_required('admin', 'staff', 'cliente')
@transaction.atomic
def finalizar_pedido(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("productos")

    total = 0
    for item in cart.values():
        total += item["price"] * item["quantity"]

    pedido = Pedido.objects.create(
        usuario=request.user,
        total=total,
        estado="PEND",
    )

    for item in cart.values():
        producto = Producto.objects.get(pk=item["product_id"])
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item["quantity"],
            precio_unitario=item["price"],
            subtotal=item["price"] * item["quantity"]
        )

    request.session["cart"] = {}
    request.session.modified = True

    messages.success(request, f"Pedido generado con éxito. Código: {pedido.codigo_pedido}")
    return redirect("pedido_exito", pedido_id=pedido.pk)


@role_required('admin', 'staff', 'cliente')
def pedido_exito(request, pedido_id):
    pedido = Pedido.objects.prefetch_related("items__producto").get(pk=pedido_id)
    return render(request, "pedido_exito.html", {"pedido": pedido})

def error_404_view(request, exception):
    return render(request, 'CestaMagica/error_404.html', status=404)
def error_500_view(request):
    return render(request, 'CestaMagica/error_500.html', status=500)
def error_403_view(request, exception):
    return render(request, 'CestaMagica/error_403.html', status=403)
def error_400_view(request, exception):
    return render(request, 'CestaMagica/error_400.html', status=400)