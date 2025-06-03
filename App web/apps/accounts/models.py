from django.db import models

#Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150) #models.EmailField(max_length=150,unique=True)
    contrasena = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True  # Esto indica que no crea tabla propia

    def __str__(self):
        return self.nombre

class Administrador(Usuario):
    pass

class Conductor(Usuario):
    tipo_licencia = models.CharField(max_length=100)

class Cliente(Usuario):
    direccion = models.CharField(max_length=300)
