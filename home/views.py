from django.shortcuts import render,redirect, get_object_or_404
from producto.models import Producto, Categoria
# import bcchapi
# import numpy as np
import requests

# Create your views here.                                                          

def home(request):

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()


    data = {
        'productos': productos,
        'categorias': categorias
    }

    return render(request,'index.html', data)


def admin(request):

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    data = {
        'productos': productos,
        'categorias': categorias
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

def eliminar(request,id):

    producto = get_object_or_404(Producto, id=id)
    producto.delete()

    return redirect(to='home:administrador')