from django.urls import path
from . import views

app_name = "producto"

urlpatterns = [

    path('categoria/<int:id>', views.productos, name='categoria'),

]