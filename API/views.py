from rest_framework import viewsets
from .serializers import ProductoSerializers, CategoriaSerializers
from producto.models import Producto,Categoria

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializers

class CategoriaViewset(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializers