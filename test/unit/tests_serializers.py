import pytest
from rest_framework.exceptions import ValidationError
from producto.models import Producto, Categoria, Marca
from API.serializers import ProductoSerializers, CategoriaSerializers, MarcaSerializers

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

# Pruebas para el serializador Categoria
@pytest.mark.django_db
def test_marca_serializer_valid():
    data = {'nombre': 'Generica'}
    serializer = MarcaSerializers(data=data)
    assert serializer.is_valid()
    marca = serializer.save()
    assert marca.nombre == 'Generica'

@pytest.mark.django_db
def test_marca_serializer_invalid():
    data = {'nombre': ''}
    serializer = MarcaSerializers(data=data)
    assert not serializer.is_valid()
    assert 'nombre' in serializer.errors

# Pruebas para el serializador Producto
@pytest.fixture
def categoria(db):
    return Categoria.objects.create(nombre='Herramientas')

# Pruebas para el serializador Producto
@pytest.fixture
def marca(db):
    return Marca.objects.create(nombre='Generica')

@pytest.mark.django_db
def test_producto_serializer_valid(categoria, marca):
    data = {
        'nombre': 'Taladro',
        'precio': 100.00,
        'descripcion': 'Un taladro potente',
        'categoria': categoria.id,
        'marca': marca.id,
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
