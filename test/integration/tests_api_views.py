import pytest
from rest_framework.test import APIClient
from producto.models import Producto, Categoria

# Fixture para el cliente de la API
@pytest.fixture
def api_client():
    return APIClient()

# Fixture para crear una categoría
@pytest.fixture
def categoria(db):
    return Categoria.objects.create(nombre='Herramientas')

# Fixture para crear un producto
@pytest.fixture
def producto(categoria, db):
    return Producto.objects.create(
        nombre='Taladro',
        precio=100.00,
        descripcion='Un taladro potente',
        categoria=categoria,
        stock=10
    )

# Pruebas para ProductoViewset
@pytest.mark.django_db
def test_get_lista_productos(api_client, producto):
    response = api_client.get('/api/producto/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['nombre'] == 'Taladro'

@pytest.mark.django_db
def test_get_detalle_producto(api_client, producto):
    response = api_client.get(f'/api/producto/{producto.id}/')
    assert response.status_code == 200
    assert response.data['nombre'] == 'Taladro'

@pytest.mark.django_db
def test_post_crear_producto(api_client, categoria):
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
def test_put_actualizar_producto(api_client, producto):
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
def test_delete_eliminar_producto(api_client, producto):
    response = api_client.delete(f'/api/producto/{producto.id}/')
    assert response.status_code == 204
    assert Producto.objects.count() == 0

# Pruebas para CategoriaViewset
@pytest.mark.django_db
def test_get_lista_categorias(api_client, categoria):
    response = api_client.get('/api/categoria/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['nombre'] == 'Herramientas'

@pytest.mark.django_db
def test_get_detalle_categoria(api_client, categoria):
    response = api_client.get(f'/api/categoria/{categoria.id}/')
    assert response.status_code == 200
    assert response.data['nombre'] == 'Herramientas'

@pytest.mark.django_db
def test_post_crear_categoria(api_client):
    data = {'nombre': 'Electrodomésticos'}
    response = api_client.post('/api/categoria/', data)
    assert response.status_code == 201
    assert response.data['nombre'] == 'Electrodomésticos'

@pytest.mark.django_db
def test_put_actualizar_categoria(api_client, categoria):
    data = {'nombre': 'Herramientas de Jardín'}
    response = api_client.put(f'/api/categoria/{categoria.id}/', data)
    assert response.status_code == 200
    assert response.data['nombre'] == 'Herramientas de Jardín'

@pytest.mark.django_db
def test_delete_eliminar_categoria(api_client, categoria):
    response = api_client.delete(f'/api/categoria/{categoria.id}/')
    assert response.status_code == 204
    assert Categoria.objects.count() == 0
