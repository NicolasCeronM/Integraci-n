from rest_framework import viewsets
from .serializers import ProductoSerializers
from producto.models import Producto

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializers