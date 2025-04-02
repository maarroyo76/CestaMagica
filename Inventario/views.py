from django.shortcuts import get_object_or_404, redirect, render
from .models import Producto, Categoria, Marca, UnidadVenta, PrecioProducto, userProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    productos_destacados = Producto.objects.filter(destacado=True)[:8]
    return render(request, 'CestaMagica/home.html', {'productos_destacados': productos_destacados})

def productos(request):
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
        productos = productos.order_by('precios__precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precios__precio')
    else:
        productos = productos.order_by('nombre')

    context = {
        'productos': productos,
        'categorias': categorias,
        'selected_categoria': categoria_id,
        'marcas': marcas,
        'selected_marca': marca,
        'search_query': search_query,
        'marca': marca,
        'categoria_id': categoria_id,
        'orden': orden
    }

    return render(request, 'CestaMagica/productos.html', context)

def retroceder(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def gestion(request):
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

    return render(request, 'CestaMagica/contacto.html')

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)

        marca_id = request.POST.get('marca')
        marca = get_object_or_404(Marca, id=marca_id)

        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        stock = request.POST.get('stock')
        imagen = request.FILES.get('imagen')

        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            stock=stock,
            categoria=categoria,
            marca=marca
        )
        if imagen:
            producto.imagen = imagen
        producto.save()

        unidades_venta = UnidadVenta.objects.all()
        for unidad in unidades_venta:
            precio_key = f"precio_{unidad.id}"
            if precio_key in request.POST:
                precio = request.POST.get(precio_key)
                if precio:
                    PrecioProducto.objects.create(
                        producto=producto,
                        unidad_venta=unidad,
                        precio=precio
                    )

        messages.success(request, 'Producto agregado correctamente')
        return redirect('gestion')

    categorias = Categoria.objects.all()
    categorias = categorias.order_by('nombre')
    marcas = Marca.objects.all()
    marcas = marcas.order_by('nombre')
    unidades_venta = UnidadVenta.objects.all()

    context = {
        'categorias': categorias,
        'marcas': marcas,
        'unidades_venta': unidades_venta
    }

    return render(request, 'CestaMagica/Gestion/agregar.html', context)

@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)

        marca_id = request.POST.get('marca')
        marca = get_object_or_404(Marca, id=marca_id)

        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion', '')
        producto.stock = request.POST.get('stock')
        producto.categoria = categoria
        producto.marca = marca
        if request.FILES.get('imagen'):
            producto.imagen = request.FILES.get('imagen')
        producto.save()

        unidades_venta = UnidadVenta.objects.all()
        for unidad in unidades_venta:
            precio_key = f"precio_{unidad.id}"
            if precio_key in request.POST:
                precio = request.POST.get(precio_key)
                if precio: 
                    precio_producto, created = PrecioProducto.objects.get_or_create(
                        producto=producto,
                        unidad_venta=unidad,
                        defaults={'precio': precio}
                    )
                    if not created:
                        precio_producto.precio = precio
                        precio_producto.save()

        messages.success(request, 'Producto editado correctamente')
        return redirect('gestion')

    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    unidades_venta = UnidadVenta.objects.all()
    precios = {pp.unidad_venta.id: pp.precio for pp in producto.precios.all()}

    context = {
        'producto': producto,
        'categorias': categorias,
        'marcas': marcas,
        'unidades_venta': unidades_venta,
        'precios': precios  
    }

    return render(request, 'CestaMagica/Gestion/editar.html', context)

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()

    messages.success(request, 'Producto eliminado correctamente')
    return redirect('gestion')


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    precios = producto.precios.all() 

    context = {
        'producto': producto,
        'precios': precios
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

        if User.objects.filter(usuario=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return render(request, "registro.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
            return render(request, "registro.html")
        
        telefono = '+56 9' + telefono.strip()
        
        newUser = userProfile(
            username=username,
            first_name=nombre,
            last_name=apellido,
            email=email,
            telefono=telefono,
            role='cliente',
        )
        newUser.set_password(password)
        newUser.save()

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
            login(request, user)
            return redirect('gestion')
        else:
            return render(request, 'CestaMagica/auth/inicio_sesion.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'CestaMagica/auth/inicio_sesion.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('login')