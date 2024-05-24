from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.home, name='home'),
    path('administrador/', views.admin, name="administrador"),
    # aciones de administrador
    path('eliminar/<id>/', views.eliminar, name="eliminar"),

    # seccion de contacto
    path('contacto/', views.contacto, name="contacto"),
    path('registro/', views.registro, name='registro'),
    path('salir/', views.salir, name='salir'),
]
