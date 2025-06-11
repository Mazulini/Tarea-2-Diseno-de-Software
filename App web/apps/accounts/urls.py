from django.urls import path
from . import views
from .views import register_view
from .decorators import require_rol

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('no-autorizado/', views.no_autorizado, name='no_autorizado'),

    path('admin/', require_rol('admin')(views.admin_dashboard), name='admin_dashboard'),
    path('cliente/', require_rol('cliente')(views.cliente_dashboard), name='cliente_dashboard'),
    path('conductor/', require_rol('conductor')(views.conductor_dashboard), name='conductor_dashboard'),

    #Admin
    path('admin/ver-usuarios/', require_rol('admin')(views.ver_usuarios), name='ver_usuarios'),
    path('admin/ver-paquetes/', require_rol('admin')(views.admin_ver_paquetes), name='admin_ver_paquetes'),
    path('admin/historial-envios/', require_rol('admin')(views.ver_historial_envios), name='ver_historial_envios'),
    path('admin/registrar-socio/', require_rol('admin')(views.registrar_socio), name='registrar_socio'),
    path('admin/gestionar-horarios/', require_rol('admin')(views.gestionar_horarios), name='gestionar_horarios'),
    path('admin/ver-rutas/', require_rol('admin')(views.admin_ver_rutas), name='admin_ver_rutas'),

    #Conductor
    path('conductor/', require_rol('conductor')(views.conductor_dashboard), name='conductor_dashboard'),
    path('conductor/conductor_ver-rutas/', require_rol('conductor')(views.conductor_ver_rutas), name='conductor_ver_rutas'),

    #Cliente
    path('cliente/enviar-paquete/', require_rol('cliente')(views.cliente_enviar_paquete), name='cliente_enviar_paquete'),
    path('cliente/ver-paquetes/', require_rol('cliente')(views.cliente_ver_paquetes), name='cliente_ver_paquetes'),

]