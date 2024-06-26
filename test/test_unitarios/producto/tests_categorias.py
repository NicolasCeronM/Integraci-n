import pytest
from producto.models import Categoria

@pytest.mark.django_db
def test_categoria_creation():
    categoria = Categoria.objects.create(

        nombre = 'test_unitario_categoria'
    ) 

    assert categoria.nombre == 'test_unitario_categoria'