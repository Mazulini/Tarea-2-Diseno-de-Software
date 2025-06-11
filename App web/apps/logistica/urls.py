from django.urls import path
from . import views

app_name = 'logistica'

urlpatterns = [
    path('paquetes/', views.lista_paquetes, name='lista_paquetes'),
    path('asignar-paquete-ruta/', views.asignar_paquete_ruta, name='asignar_paquete_ruta'),
    path('asignar-ruta-conductor/', views.asignar_ruta_conductor, name='asignar_ruta_conductor'),
]