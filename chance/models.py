from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
import datetime

from django.utils import timezone
class LotoChance(models.Model):
    nombre = models.CharField(max_length=255)
    thumb = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-loto.jpg')
    created_at = models.DateTimeField(editable=False)
    active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)    

class VentaChance(models.Model):
    fecha = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(editable=False)
    active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)    

class DetalleVentaChance(models.Model):
    propietario = models.ForeignKey(VentaChance, on_delete=models.CASCADE)
    numero = models.CharField(max_length=4)
    loterias = models.ManyToManyField(LotoChance)
    monto = models.CharField(max_length=20)
    created_at = models.DateTimeField(editable=False)
    active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)    

class TemporalChance(models.Model):
    fecha = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    numero = models.CharField(max_length=4)
    loterias = models.ManyToManyField(LotoChance)
    monto = models.CharField(max_length=20)
    total = models.CharField(max_length=20,blank=True)
    created_at = models.DateTimeField(editable=False)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)    
