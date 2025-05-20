from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .carro import Carro
from producto.models import Producto, Direccion, Categoria
import mercadopago
from django.conf import settings
import requests
from carro.context_processor import importe_total_carro
from django.contrib.auth.decorators import login_required

# Create your views here.

def vista_carro(request):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    carro = Carro(request)

    if not carro.carro:
        return render(request, 'carro.html')

    # Si se envía nueva dirección
    if request.method == 'POST':
        Direccion.objects.create(
            user=request.user,
            nombre=request.POST['nombre'],
            region=request.POST['region'],
            comuna=request.POST['comuna'],
            calle=request.POST['calle'],
            numero=request.POST['numero'],
            dep=request.POST['casa']
        )

    # Construir los items del carrito
    items = []
    for key, producto in carro.carro.items():
        items.append({
            "title": producto['nombre'],
            "quantity": producto['cantidad'],
            "currency_id": "CLP",
            "unit_price": float(producto['precio']),
            "description": f"Producto {producto['nombre']}"
        })

    # Variables adicionales
    direccion_id = request.session.get('direccion_id')
    direccion_envio = Direccion.objects.filter(id=direccion_id)
    direcciones = Direccion.objects.all()
    categorias = Categoria.objects.all()
    preference_id = None

    # Solo generamos preferencia si hay dirección confirmada
    if direccion_id:
        preference_data = {
            "items": items,
            "payer": {
                "email": "test_user_1291106205@testuser.com"
            },
            "back_urls": {
                "success": "https://rpst7h3c-8000.brs.devtunnels.ms/mis_compras",
                "failure": "http://localhost:8000/",
                "pending": "http://localhost:8000/"
            },
            "auto_return": "approved"  # Comentado para evitar error con localhost
        }

        try:
            preference_response = sdk.preference().create(preference_data)
           # print("💥 DEBUG - Respuesta completa:", preference_response)
           # print("🔧 Datos enviados a MercadoPago:", preference_data)

            preference = preference_response.get("response", {})
            preference_id = preference.get("id")
            print("✅ Preferencia generada:", preference_id)

        except Exception as e:
            print("❌ Error al generar preferencia:", str(e))
            preference_id = None


    return render(request, 'carro.html', {
        'preference_id': preference_id,
        'public_key': settings.MERCADO_PAGO_PUBLIC_KEY,
        'direcciones': direcciones,
        'categorias': categorias,
        'direccion_id': direccion_id,
        'direccion_envio': direccion_envio,
    })


    
@login_required
def agregar_producto(request,producto_id):

    carro = Carro(request)
    producto = Producto.objects.get(id=producto_id)
            
    carro.agregar(producto = producto)


    return redirect("carro:carro")

# def eliminiar_producto(request,producto_id):

#     carro = Carro(request)

#     producto = Producto.objects.get(id=producto_id)

#     carro.eliminar(producto = producto)

#     return redirect("carro:carro")

# def restar_producto(request,producto_id):

#     carro = Carro(request)

#     producto = Producto.objects.get(id=producto_id)

#     carro.restar_producto(producto = producto)

#     return redirect("carro:carro")

def limpiar_carro(request):

    carro = Carro(request)
    carro.limpiar_carro()

    return redirect("carro:carro")


# PRUEBAS AJAX


def calcular_total(carro):
    total = 0
    for key, value in carro.carro.items():
        total += int(value['precio']) * value['cantidad']
    return total


def sumar_producto(request, producto_id):
    try:
        carro = Carro(request)
        producto = Producto.objects.get(id=producto_id)
        carro.agregar(producto = producto)
        cantidad = carro.carro[str(producto.id)]['cantidad']
        total = calcular_total(carro)
        return JsonResponse({'message': 'Producto sumado', 'cantidad': cantidad, 'total': total})
    except Producto.DoesNotExist:
        return JsonResponse({'message': 'Producto no encontrado'}, status=404)
    except KeyError as e:
        return JsonResponse({'message': f'Error al sumar producto: {e}'}, status=500)

@login_required
def restar_producto(request, producto_id):
    try:
        carro = Carro(request)
        producto = Producto.objects.get(id=producto_id)
        carro.restar_producto(producto=producto)
        cantidad = carro.carro[str(producto.id)]['cantidad'] if str(producto.id) in carro.carro else 0
        total = calcular_total(carro)
        return JsonResponse({'message': 'Producto restado', 'cantidad': cantidad, 'total': total})
    except Producto.DoesNotExist:
        return JsonResponse({'message': 'Producto no encontrado'}, status=404)
    except KeyError as e:
        return JsonResponse({'message': f'Error al restar producto: {e}'}, status=500)

@login_required
def eliminar_producto(request, producto_id):
    try:
        carro = Carro(request)
        producto = Producto.objects.get(id=producto_id)
        carro.eliminar(producto=producto)
        total = calcular_total(carro)
        return JsonResponse({'message': 'Producto eliminado', 'total': total})
    except Producto.DoesNotExist:
        return JsonResponse({'message': 'Producto no encontrado'}, status=404)
    except KeyError as e:
        return JsonResponse({'message': f'Error al eliminar producto: {e}'}, status=500)

def confirmar_direccion(request):
    if request.method == 'POST':
        direccion_id = request.POST.get('direccion')
        if direccion_id:
            request.session['direccion_id'] = direccion_id
        return redirect('carro:carro') 
    
def cambiar_direccion(request):
    del request.session['direccion_id']
    return redirect('carro:carro') 