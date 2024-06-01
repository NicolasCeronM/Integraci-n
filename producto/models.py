from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):

    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to='producto', null=True, blank=True)
    stock = models.IntegerField(null=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='pedidos')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()

    def __str__(self):

        return str(self.id)
    

    class Meta:
        db_table = 'pedidos' #Como se va a ver en la basen de datos
        verbose_name ='pedido'
        verbose_name_plural ='pedidos'
    
    
class DetallePedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='detalle_pedido')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles_pedido')
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles_pedido')
    cantidad = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} unidades de {self.producto}'

    class Meta:
        db_table = 'detalle_pedido'  # Cómo se verá en la base de datos
        verbose_name = 'detalle_pedido'
        verbose_name_plural = 'detalle_pedidos'