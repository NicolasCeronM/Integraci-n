from django.urls import path
from . import views

app_name = "carro"

urlpatterns = [

    path('', views.vista_carro, name='carro'),
    path('agregar/<int:producto_id>',views.agregar_producto, name='agregar'),
    # path('eliminar/<int:producto_id>',views.eliminiar_producto, name='eliminar'),
    # path('restar/<int:producto_id>',views.restar_producto, name='restar'),
    # path('limpiar/',views.limpiar_carro, name='limpiar'),

    path('sumar_producto/<int:producto_id>/',views.sumar_producto, name='sumar_producto'),
    path('eliminar/<int:producto_id>/',views.eliminar_producto, name='eliminar'),
    path('restar/<int:producto_id>',views.restar_producto, name='restar'),
    path('limpiar/',views.limpiar_carro, name='limpiar')
]