from django.shortcuts import render, redirect
from .carro import Carro
from producto.models import Producto

# Create your views here.
def vista_carro(request):

    return render(request,'carro.html')
    
def agregar_producto(request,producto_id):

    carro = Carro(request)
    producto = Producto.objects.get(id=producto_id)
            
    carro.agregar(producto = producto)


    return redirect("carro:carro")

def eliminiar_producto(request,producto_id):

    carro = Carro(request)

    producto = Producto.objects.get(id=producto_id)

    carro.eliminar(producto = producto)

    return redirect("index")

def restar_producto(request,producto_id):

    carro = Carro(request)

    producto = Producto.objects.get(id=producto_id)

    carro.restar_producto(producto = producto)

    return redirect("dashboard:carro")

def limpiar_carro(request):

    carro = Carro(request)
    carro.limpiar_carro()

    return redirect("dashboard:carro")