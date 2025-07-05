# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

#Tablas de accounts

class Usuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(unique=True, max_length=150)
    contrasena = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField()
    rol = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usuario'


class Admin(models.Model):
    usuario = models.OneToOneField('Usuario', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Cliente(models.Model):
    usuario = models.OneToOneField('Usuario', models.DO_NOTHING, primary_key=True)
    direccion = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'cliente'


class Conductor(models.Model):
    usuario = models.OneToOneField('Usuario', models.DO_NOTHING, primary_key=True)
    tipo_licencia = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'conductor'

#Tablas de logistica

class Envio(models.Model):
    ruta = models.ForeignKey('Ruta', models.DO_NOTHING)
    conductor = models.ForeignKey(Conductor, models.DO_NOTHING, null=True)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'envio'

class EnvioPaquete(models.Model):
    envio = models.ForeignKey('Envio', models.DO_NOTHING)
    paquete = models.ForeignKey('Paquete', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'envio_paquete'
        unique_together = (('envio', 'paquete'),)

    def __str__(self):
        return f"Envío {self.envio.id} - Paquete {self.paquete.id}"

class EstadisticaRuta(models.Model):
    ruta = models.ForeignKey('Ruta', models.DO_NOTHING)
    conductor = models.ForeignKey(Conductor, models.DO_NOTHING)
    fecha_periodo = models.DateField()
    tiempo_real_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    distancia_recorrida_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    eficiencia = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'estadistica_ruta'
        unique_together = (('ruta', 'fecha_periodo'),)

class EstadoDeEntrega(models.Model):
    nombre_estado = models.CharField(unique=True, max_length=50)
    class Meta:
        managed = False
        db_table = 'estado_de_entrega'

class HistorialEstados(models.Model):
    paquete = models.ForeignKey('Paquete', models.DO_NOTHING)
    estado = models.ForeignKey(EstadoDeEntrega, models.DO_NOTHING)
    fecha_cambio = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'historial_estados'

class Notificacion(models.Model):
    envio = models.ForeignKey(Envio, models.DO_NOTHING)
    paquete = models.ForeignKey('Paquete', models.DO_NOTHING)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField()
    leido = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'notificacion'

class Paquete(models.Model):
    remitente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='remitente', related_name='paquetes_enviados')
    tipo = models.CharField(max_length=100)
    contenido = models.TextField(blank=True, null=True)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    dimensiones = models.CharField(max_length=50, blank=True, null=True)
    destinatario = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='destinatario', related_name='paquetes_recibidos')
    estado_entrega = models.ForeignKey(EstadoDeEntrega, models.DO_NOTHING, db_column='estado_entrega')
    class Meta:
        managed = False
        db_table = 'paquete'

class Reporte(models.Model):
    conductor = models.ForeignKey(Conductor, models.DO_NOTHING)
    ruta = models.ForeignKey('Ruta', models.DO_NOTHING)
    fecha_generacion = models.DateTimeField()
    contenido = models.CharField(max_length=500)
    class Meta:
        managed = False
        db_table = 'reporte'

class Ruta(models.Model):
    origen = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    distancia_recorrida = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora_prevista = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'ruta'