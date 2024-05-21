from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from .carro import Carro
from producto.models import Producto
import mercadopago
from django.conf import settings
import requests
from carro.context_processor import importe_total_carro


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
            "success": "http://localhost:8000/",
            "failure": "http://localhost:8000/failure/",
            "pending": "http://localhost:8000/pending/"
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    return render(request, 'carro.html', {
        'preference_id': preference['id'],
        'public_key': settings.MERCADO_PAGO_PUBLIC_KEY,
    })

def cambiar_moneda(request):
    # Obtener el total del carro desde el context processor
    monedas_disponibles = []

    # Obtener lista de monedas disponibles
    response = requests.get(f'https://v6.exchangerate-api.com/v6/{api_key}/codes')
    if response.status_code == 200:
        supported_codes = response.json().get('supported_codes', [])
        monedas_disponibles = [(code, name) for code, name in supported_codes]

    numero_convertido = None
    moneda_seleccionada = None

    context = importe_total_carro(request)
    total_carro = context['importe_total_carro']

    if request.method == 'POST':
        moneda_seleccionada = request.POST.get('moneda', 'CLP')
        cantidad = total_carro

        # Obtener tasas de cambio
        response = requests.get(f'https://v6.exchangerate-api.com/v6/{api_key}/latest/CLP')
        exchange_rates = response.json().get('conversion_rates', {})

        # Convertir la cantidad a la moneda seleccionada
        tasa_cambio = exchange_rates.get(moneda_seleccionada, 1)
        numero_convertido = cantidad * tasa_cambio

    return render(request, 'cambio_moneda.html', {
        'moneda_seleccionada': moneda_seleccionada,
        'numero_convertido': numero_convertido,
        'total_carro': total_carro,
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