import pytest
from django.http import HttpRequest
from producto.models import Producto, Categoria
from carro.carro import Carro

carro = Carro

@pytest.mark.django_db
def categoria():
    return Categoria.objects.create(nombre='Herramientas')

@pytest.mark.django_db
def producto(categoria):
    return Producto.objects.create(
        nombre='Taladro',
        precio=100.00,
        descripcion='Un taladro potente',
        categoria=categoria,
        stock=10
    )

@pytest.mark.django_db
def test_agregar_producto(producto):
    carro.agregar(producto)
    assert str(producto.id) in carro.carro
    assert carro.carro[str(producto.id)]['cantidad'] == 1

@pytest.mark.django_db
def test_agregar_mismo_producto(carro, producto):
    carro.agregar(producto)
    carro.agregar(producto)
    assert str(producto.id) in carro.carro
    assert carro.carro[str(producto.id)]['cantidad'] == 2

@pytest.mark.django_db
def test_restar_producto(carro, producto):
    carro.agregar(producto)
    carro.agregar(producto)
    carro.restar_producto(producto)
    assert carro.carro[str(producto.id)]['cantidad'] == 1

@pytest.mark.django_db
def test_restar_producto_hasta_eliminar(carro, producto):
    carro.agregar(producto)
    carro.restar_producto(producto)
    assert str(producto.id) not in carro.carro

@pytest.mark.django_db
def test_eliminar_producto(carro, producto):
    carro.agregar(producto)
    carro.eliminar(producto)
    assert str(producto.id) not in carro.carro

@pytest.mark.django_db
def test_limpiar_carro(carro, producto):
    carro.agregar(producto)
    carro.limpiar_carro()
    assert carro.carro == {}
