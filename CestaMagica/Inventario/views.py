from django.shortcuts import get_object_or_404, redirect, render
from .models import Producto, Categoria, Marca

# Create your views here.

def home(request):
    productos = Producto.objects.all()
    return render(request, 'CestaMagica/home.html', {'productos': productos})

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'CestaMagica/productos.html', {'productos': productos})

def gestion(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    
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
    return render(request, 'CestaMagica/contacto.html')

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
        
        return redirect('gestion')
        
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    return render(request, 'CestaMagica/Gestion/agregar.html',  {'categorias': categorias, 'marcas': marcas})

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
    return redirect('gestion')
