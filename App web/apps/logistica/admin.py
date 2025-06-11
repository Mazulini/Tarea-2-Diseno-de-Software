from django.contrib import admin
from .models import Usuario, Cliente, Conductor, Admin, Ruta, Envio, Paquete, EnvioPaquete, EstadoDeEntrega, HistorialEstados, Notificacion, Reporte, EstadisticaRuta

# Register your models here
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Conductor)
admin.site.register(Admin)
admin.site.register(Ruta)
admin.site.register(Envio)
admin.site.register(Paquete)
admin.site.register(EnvioPaquete)
admin.site.register(EstadoDeEntrega)
admin.site.register(HistorialEstados)
admin.site.register(Notificacion)
admin.site.register(Reporte)
admin.site.register(EstadisticaRuta)