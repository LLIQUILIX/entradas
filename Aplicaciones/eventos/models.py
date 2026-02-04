from django.db import models
import uuid

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.DateField()  
    hora_inicio = models.TimeField()
    capacidad_total = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.FileField(upload_to='flayers')

    @property
    def entradas_disponibles(self):
        vendidas = self.entrada_set.count()
        return self.capacidad_total - vendidas

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=10)

class Entrada(models.Model):
    id_unico = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)