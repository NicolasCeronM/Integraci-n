import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from producto.models import Producto, Categoria

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def categoria():
    return Categoria.objects.create(nombre='Herramientas')

@pytest.fixture
def producto(categoria):
    return Producto.objects.create(
        nombre='Taladro',
        precio=100.00,
        descripcion='que hace un perro con un taladro ta ladrando ajsajsas necesito amigos',
        categoria=categoria,
        stock=10
    )

@pytest.mark.django_db
def test_get_productos(api_client, producto):
    response = api_client.get('/api/producto/')
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_get_producto_detail(api_client, producto):
    response = api_client.get(f'/api/producto/{producto.id}/')
    assert response.status_code == 200
    assert response.data['nombre'] == 'Taladro'

@pytest.mark.django_db
def test_post_producto(api_client, categoria):
    data = {
        'nombre': 'Martillo',
        'precio': 50.00,
        'descripcion': 'Un martillo resistente',
        'categoria': categoria.id,
        'stock': 15
    }
    response = api_client.post('/api/producto/', data)
    assert response.status_code == 201
    assert response.data['nombre'] == 'Martillo'

@pytest.mark.django_db
def test_put_producto(api_client, producto):
    data = {
        'nombre': 'Taladro Inalámbrico',
        'precio': 150.00,
        'descripcion': 'Un taladro potente y sin cables',
        'categoria': producto.categoria.id,
        'stock': 5
    }
    response = api_client.put(f'/api/producto/{producto.id}/', data)
    assert response.status_code == 200
    assert response.data['nombre'] == 'Taladro Inalámbrico'

@pytest.mark.django_db
def test_delete_producto(api_client, producto):
    response = api_client.delete(f'/api/producto/{producto.id}/')
    assert response.status_code == 204
    assert Producto.objects.count() == 0

@pytest.mark.django_db
def test_get_categorias(api_client, categoria):
    response = api_client.get('/api/categoria/')
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_get_categoria_detail(api_client, categoria):
    response = api_client.get(f'/api/categoria/{categoria.id}/')
    assert response.status_code == 200
    assert response.data['nombre'] == 'Herramientas'

@pytest.mark.django_db
def test_post_categoria(api_client):
    data = {'nombre': 'Electrodomésticos'}
    response = api_client.post('/api/categoria/', data)
    assert response.status_code == 201
    assert response.data['nombre'] == 'Electrodomésticos'

@pytest.mark.django_db
def test_put_categoria(api_client, categoria):
    data = {'nombre': 'Herramientas de Jardín'}
    response = api_client.put(f'/api/categoria/{categoria.id}/', data)
    assert response.status_code == 200
    assert response.data['nombre'] == 'Herramientas de Jardín'

@pytest.mark.django_db
def test_delete_categoria(api_client, categoria):
    response = api_client.delete(f'/api/categoria/{categoria.id}/')
    assert response.status_code == 204
    assert Categoria.objects.count() == 0
