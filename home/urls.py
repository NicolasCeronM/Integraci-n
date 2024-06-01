from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.home, name='home'),
    path('administrador/', views.admin, name="administrador"),
    # session de administrador
    path('eliminar/<id>/', views.eliminar, name="eliminar"),
    # seccion de usuario
    path('mis_compras/', views.vista_usuario, name='mis_compras'),

    # seccion de contacto
    path('contacto/', views.contacto, name="contacto"),
    path('registro/', views.registro, name='registro'),
    path('salir/', views.salir, name='salir'),
]
