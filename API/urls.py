from django.urls import path, include
from .views import ProductoViewset
from rest_framework import routers

router = routers.DefaultRouter()

router.register('producto',ProductoViewset)

urlpatterns = [
    path('', include(router.urls)),
]