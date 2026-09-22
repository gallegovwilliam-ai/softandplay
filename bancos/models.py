from django.db import models
import datetime

from django.utils import timezone
class Banco(models.Model):
    
    moneda = models.CharField(max_length=255)
    corresponsal = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    codigo_swift = models.CharField(max_length=255,blank=True)
    banco_benef = models.CharField(max_length=255)
    cuenta = models.CharField(max_length=255)
    beneficiario_final = models.CharField(max_length=255)
    cuenta_abono = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)    
