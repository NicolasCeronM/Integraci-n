import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from producto.models import Producto, Categoria, Pedido, DetallePedido, Direccion

# Fixture para crear un usuario
@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

# Fixture para el cliente autenticado
@pytest.fixture
def client(user):
    client = Client()
    client.login(username='testuser', password='testpass')
    return client

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

# Fixture para crear una dirección
@pytest.fixture
def direccion(user, db):
    return Direccion.objects.create(
        user=user,
        nombre='Casa',
        region='Region',
        comuna='Comuna',
        calle='Calle',
        numero=123
    )

# Pruebas para home
@pytest.mark.django_db
def test_home_view(client, producto):
    response = client.get(reverse('home:home'))
    assert response.status_code == 200
    assert 'Taladro' in response.content.decode()

# Pruebas para admin
@pytest.mark.django_db
def test_admin_view(client, user, producto):
    user.is_staff = True
    user.save()
    response = client.get(reverse('home:administrador'))
    assert response.status_code == 200
    assert 'Taladro' in response.content.decode()

# Pruebas para admin_pedido
@pytest.mark.django_db
def test_admin_pedido_view(client, user, direccion, producto):
    user.is_staff = True
    user.save()
    pedido = Pedido.objects.create(user=user, direccion=direccion, total=100.00)
    DetallePedido.objects.create(user=user, producto=producto, pedido=pedido, cantidad=2)
    response = client.get(reverse('home:pedidos'))
    assert response.status_code == 200
    assert str(pedido.id) in response.content.decode()

# Pruebas para eliminar
@pytest.mark.django_db
def test_eliminar_producto_view(client, producto):
    response = client.post(reverse('home:eliminar', args=[producto.id]))
    assert response.status_code == 302  # Verifica redirección después de eliminar
    assert Producto.objects.count() == 0

# Pruebas para contacto
@pytest.mark.django_db
def test_contacto_view(client):
    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'subject': 'Test Subject',
        'message': 'Test message'
    }
    response = client.post(reverse('home:contacto'), data)
    assert response.status_code == 302  # Verifica redirección después de enviar el contacto
    

# Pruebas para registro
@pytest.mark.django_db
def test_registro_view(client):
    data = {
        'username': 'newuser',
        'password1': 'testpassword',
        'password2': 'testpassword'
    }
    response = client.post(reverse('home:registro'), data)
    assert response.status_code == 302  # Verifica redirección después del registro
    user = User.objects.get(username='newuser')
    assert user is not None

# Pruebas para vista_usuario
@pytest.mark.django_db
def test_vista_usuario_view(client, user, direccion, producto):
    pedido = Pedido.objects.create(user=user, direccion=direccion, total=100.00)
    DetallePedido.objects.create(user=user, producto=producto, pedido=pedido, cantidad=2)
    response = client.get(reverse('home:mis_compras'))
    assert response.status_code == 200
    assert str(pedido.id) in response.content.decode()

# Pruebas para salir
@pytest.mark.django_db
def test_salir_view(client):
    response = client.get(reverse('home:salir'))
    assert response.status_code == 302  # Verifica redirección después del logout
