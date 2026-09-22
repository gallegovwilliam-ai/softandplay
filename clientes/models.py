from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.translation import gettext_lazy as _


from django.utils import timezone
class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    nombre = models.CharField(max_length=50, blank=True)
    apellido = models.CharField(max_length=50, blank=True)
    dni = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)
    create_at = models.DateTimeField(editable=False,)
    def save(self, *args, **kwargs):
        if not self.id:
            self.create_at = timezone.now()
        return super().save(*args, **kwargs)    
    def __str__(self):
        return self.nombre
    class Meta:
        ordering = ['-id']
