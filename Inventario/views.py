from django.shortcuts import get_object_or_404, redirect, render
from .models import Producto, Categoria, Marca
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

def home(request):
    productos_destacados = Producto.objects.filter(destacado=True)[:8]
    return render(request, 'CestaMagica/home.html', {'productos_destacados': productos_destacados})

def productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    categorias = categorias.order_by('nombre')
    marcas = Marca.objects.all()
    marcas = marcas.order_by('nombre')

    search_query = request.GET.get('search', '')
    marca = request.GET.get('marca', '') 
    categoria_id = request.GET.get('categoria', '')
    orden = request.GET.get('orden', 'nombre')


    # Filtrar productos
    if search_query:
        productos = productos.filter(nombre__icontains=search_query)
    
    if marca:
        productos = productos.filter(marca__nombre__icontains=marca)
    else:
        productos = productos.filter(marca_id=marca)

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
        precio = request.POST.get('precio')
        imagen = request.FILES.get('imagen')

        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            stock=stock,
            precio=precio,
            categoria=categoria,
            marca=marca
        )
        if imagen:
            producto.imagen = imagen
        producto.save()
        
        messages.success(request, 'Producto agregado correctamente')
        return redirect('gestion')
        
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    return render(request, 'CestaMagica/Gestion/agregar.html',  {'categorias': categorias, 'marcas': marcas})

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
        'producto': producto,
        'categorias': Categoria.objects.all(),
        'marcas': Marca.objects.all()
    }

    return render(request, 'CestaMagica/Gestion/editar.html', context)

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()

    messages.success(request, 'Producto eliminado correctamente')
    return redirect('gestion')


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    print(producto.imagen.url)
    return render(request, 'CestaMagica/detalle.html', {'producto': producto})

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