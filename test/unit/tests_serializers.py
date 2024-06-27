import pytest
from rest_framework.exceptions import ValidationError
from producto.models import Producto, Categoria
from API.serializers import ProductoSerializers, CategoriaSerializers

# Pruebas para el serializador Categoria
@pytest.mark.django_db
def test_categoria_serializer_valid():
    data = {'nombre': 'Herramientas'}
    serializer = CategoriaSerializers(data=data)
    assert serializer.is_valid()
    categoria = serializer.save()
    assert categoria.nombre == 'Herramientas'

@pytest.mark.django_db
def test_categoria_serializer_invalid():
    data = {'nombre': ''}
    serializer = CategoriaSerializers(data=data)
    assert not serializer.is_valid()
    assert 'nombre' in serializer.errors

# Pruebas para el serializador Producto
@pytest.fixture
def categoria(db):
    return Categoria.objects.create(nombre='Herramientas')

@pytest.mark.django_db
def test_producto_serializer_valid(categoria):
    data = {
        'nombre': 'Taladro',
        'precio': 100.00,
        'descripcion': 'Un taladro potente',
        'categoria': categoria.id,
        'stock': 10
    }
    serializer = ProductoSerializers(data=data)
    assert serializer.is_valid()
    producto = serializer.save()
    assert producto.nombre == 'Taladro'
    assert producto.precio == 100.00
    assert producto.descripcion == 'Un taladro potente'
    assert producto.categoria == categoria
    assert producto.stock == 10

@pytest.mark.django_db
def test_producto_serializer_invalid(categoria):
    data = {
        'nombre': '',
        'precio': 'cien',
        'descripcion': 'Un taladro potente',
        'categoria': categoria.id,
        'stock': 10
    }
    serializer = ProductoSerializers(data=data)
    assert not serializer.is_valid()
    assert 'nombre' in serializer.errors
    assert 'precio' in serializer.errors
