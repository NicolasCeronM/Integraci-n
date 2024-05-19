from django.shortcuts import render, redirect
from .carro import Carro
from producto.models import Producto
import mercadopago
from django.conf import settings

# Create your views here.
def vista_carro(request):

    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

     # Instancia del carrito de compras
    carro = Carro(request)

    # Verificar si el carrito está vacío
    if not carro.carro:
        # Redirigir a una página de productos o mostrar un mensaje de carrito vacío
        return render(request, 'carro.html')

    # Construir el atributo "items" basado en los productos del carrito
    items = []
    for key, producto in carro.carro.items():
        item = {
            "title": producto['nombre'],  
            "quantity": producto['cantidad'],  
            "currency_id": "CLP",  
            "unit_price": float(producto['precio'])  
        }
        items.append(item)
    
    preference_data = {
        "items": items,
        "payer": {  
            "email": "test_user@test.com"
        },
        "back_urls": {
            "success": "http://localhost:8000/success/",
            "failure": "http://localhost:8000/failure/",
            "pending": "http://localhost:8000/pending/"
        },
        "auto_return": "approved"
    }
    
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    return render(request, 'carro.html', {
        'preference_id': preference['id'],
        'public_key': settings.MERCADO_PAGO_PUBLIC_KEY
    })

    
def agregar_producto(request,producto_id):

    carro = Carro(request)
    producto = Producto.objects.get(id=producto_id)
            
    carro.agregar(producto = producto)


    return redirect("carro:carro")

def eliminiar_producto(request,producto_id):

    carro = Carro(request)

    producto = Producto.objects.get(id=producto_id)

    carro.eliminar(producto = producto)

    return redirect("carro:carro")

def restar_producto(request,producto_id):

    carro = Carro(request)

    producto = Producto.objects.get(id=producto_id)

    carro.restar_producto(producto = producto)

    return redirect("carro:carro")

def limpiar_carro(request):

    carro = Carro(request)
    carro.limpiar_carro()

    return redirect("carro:carro")