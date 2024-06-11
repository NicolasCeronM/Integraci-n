import pytest
from producto.models import Producto, Categoria



@pytest.mark.django_db
def tests_producto_creations():
    categoria = Categoria.objects.create(

        nombre = 'test_unitario_categoria'
    ) 

    producto = Producto.objects.create(
        nombre = 'test_producto_nombre',
        precio = 23000,
        descripcion = 'test_producto_descripcion',
        categoria = categoria,
        stock = 23,
    )

    assert producto.nombre == 'test_producto_nombre'