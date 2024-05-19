from django.shortcuts import render
from producto.models import Producto, Categoria

# Create your views here.

def home(request):

    productos = Producto.objects.all()

    data = {
        'productos': productos
    }

    return render(request,'index.html', data)


def admin(request):

    productos = Producto.objects.all()

    data = {
        'productos': productos
    }


    if request.method != 'POST':
        return render(request,'administrador/admin.html',data)
    else:
        imagen = request.FILES.get('imagen')
        nombre = request.POST['nombre']
        descipcion = request.POST['desc']
        seccion = request.POST['seccion']
        precio = request.POST['precio']

        categoria = Categoria.objects.get(nombre=seccion)
    

        objProducto = Producto.objects.create(
            imagen = imagen,
            nombre = nombre,
            descripcion = descipcion,
            precio = precio,
            categoria = categoria,
            # stock = stock,
        )
        objProducto.save()

        # messages.success(request,'Producto creado correctamente')

        # return redirect(to='admin_page:productos')
    
        return render(request,'administrador/admin.html', data)