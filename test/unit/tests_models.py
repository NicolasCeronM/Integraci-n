import pytest
from django.contrib.auth.models import User
from producto.models import Producto, Categoria, Pedido, DetallePedido, Direccion, Marca

# Pruebas para el modelo Categoria
@pytest.mark.django_db
def test_categoria_creation():
    categoria = Categoria.objects.create(nombre='Herramientas')
    assert categoria.nombre == 'Herramientas'
    assert str(categoria) == 'Herramientas'

# Pruebas para el modelo Producto
@pytest.mark.django_db
def test_producto_creation():
    categoria = Categoria.objects.create(nombre='Herramientas')
    marca = Marca.objects.create(nombre='Generica')
    producto = Producto.objects.create(
        nombre='Taladro',
        precio=100.00,
        descripcion='Un taladro potente',
        categoria=categoria,
        marca = marca,
        stock=10
    )
    assert producto.nombre == 'Taladro'
    assert producto.precio == 100.00
    assert producto.descripcion == 'Un taladro potente'
    assert producto.categoria == categoria
    assert producto.marca == marca
    assert producto.stock == 10
    assert str(producto) == 'Taladro'

# Pruebas para el modelo Direccion
@pytest.mark.django_db
def test_direccion_creation():
    user = User.objects.create_user(username='testuser', password='testpass')
    direccion = Direccion.objects.create(
        user=user,
        nombre='Casa',
        region='Region',
        comuna='Comuna',
        calle='Calle',
        numero=123,
        dep='Departamento'
    )
    assert direccion.user == user
    assert direccion.nombre == 'Casa'
    assert direccion.region == 'Region'
    assert direccion.comuna == 'Comuna'
    assert direccion.calle == 'Calle'
    assert direccion.numero == 123
    assert direccion.dep == 'Departamento'
    assert str(direccion) == 'Casa'

# Pruebas para el modelo Pedido
@pytest.mark.django_db
def test_pedido_creation():
    user = User.objects.create_user(username='testuser', password='testpass')
    direccion = Direccion.objects.create(
        user=user,
        nombre='Casa',
        region='Region',
        comuna='Comuna',
        calle='Calle',
        numero=123
    )
    pedido = Pedido.objects.create(
        user=user,
        direccion=direccion,
        total=100.00
    )
    assert pedido.user == user
    assert pedido.direccion == direccion
    assert pedido.total == 100.00
    assert str(pedido) == str(pedido.id)

# Pruebas para el modelo DetallePedido
@pytest.mark.django_db
def test_detalle_pedido_creation():
    user = User.objects.create_user(username='testuser', password='testpass')
    categoria = Categoria.objects.create(nombre='Herramientas')
    marca = Marca.objects.create(nombre='Generica')
    producto = Producto.objects.create(
        nombre='Taladro',
        precio=100.00,
        descripcion='Un taladro potente',
        categoria=categoria,
        marca=marca,
        stock=10
    )
    direccion = Direccion.objects.create(
        user=user,
        nombre='Casa',
        region='Region',
        comuna='Comuna',
        calle='Calle',
        numero=123
    )
    pedido = Pedido.objects.create(
        user=user,
        direccion=direccion,
        total=100.00
    )
    detalle_pedido = DetallePedido.objects.create(
        user=user,
        producto=producto,
        pedido=pedido,
        cantidad=2
    )
    assert detalle_pedido.user == user
    assert detalle_pedido.producto == producto
    assert detalle_pedido.pedido == pedido
    assert detalle_pedido.cantidad == 2
    assert str(detalle_pedido) == f'{detalle_pedido.cantidad} unidades de {detalle_pedido.producto}'
