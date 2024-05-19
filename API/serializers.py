from producto.models import Producto, Categoria
from rest_framework import serializers

class ProductoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class CategoriaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'