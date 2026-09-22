from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from partidas.models import Partida, Partida75
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Carton(models.Model):
    l1_1 = models.CharField(max_length=2, blank=True)  
    l1_2 = models.CharField(max_length=2, blank=True)  
    l1_3 = models.CharField(max_length=2, blank=True)  
    l1_4 = models.CharField(max_length=2, blank=True)  
    l2_1 = models.CharField(max_length=2, blank=True)  
    l2_2 = models.CharField(max_length=2, blank=True)  
    l2_3 = models.CharField(max_length=2, blank=True)  
    l2_4 = models.CharField(max_length=2, blank=True)  
    l3_1 = models.CharField(max_length=2, blank=True)  
    l3_2 = models.CharField(max_length=2, blank=True)  
    l3_3 = models.CharField(max_length=2, blank=True)  
    l3_4 = models.CharField(max_length=2, blank=True)  
    l4_1 = models.CharField(max_length=2, blank=True)  
    l4_2 = models.CharField(max_length=2, blank=True)  
    l4_3 = models.CharField(max_length=2, blank=True)  
    l4_4 = models.CharField(max_length=2, blank=True)  

class CabezeraImpre(models.Model):
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuenta = models.CharField(max_length=30,blank=True)  
    banco = models.CharField(max_length=50, blank=True)  
    referencia = models.CharField(max_length=20, blank=True)  
    cantidad = models.PositiveIntegerField(default=0)  
    file = models.ImageField(upload_to = 'captures_bancos/')
    verficado = models.BooleanField(default=False)    


class Impresion(models.Model):
    propietario = models.ForeignKey(CabezeraImpre, on_delete=models.CASCADE)
    ganador_1 = models.BooleanField(default=False)
    posible_1 = models.BooleanField(default=False)
    ganador_2 = models.BooleanField(default=False)
    posible_2 = models.BooleanField(default=False)
    ganador_3 = models.BooleanField(default=False)
    posible_3 = models.BooleanField(default=False)
    ganador_4 = models.BooleanField(default=False)
    posible_4 = models.BooleanField(default=False)
    ganador_5 = models.BooleanField(default=False)
    posible_5 = models.BooleanField(default=False)
    ganador_6 = models.BooleanField(default=False)
    posible_6 = models.BooleanField(default=False)
    ganador_7 = models.BooleanField(default=False)
    posible_7 = models.BooleanField(default=False)
    ganador_8 = models.BooleanField(default=False)
    posible_8 = models.BooleanField(default=False)
    linea = models.IntegerField(default = 0)
    ganador_9 = models.BooleanField(default=False)
    posible_9 = models.BooleanField(default=False)
    ganador_10 = models.BooleanField(default=False)
    posible_10 = models.BooleanField(default=False)
    ganador = models.BooleanField(default=False)
    ganador_at = models.DateTimeField(blank=False, null=True)
    carton = models.ForeignKey(Carton,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False,blank=False, null=True)
    enJuego = models.BooleanField(default=False)
    pago = models.BooleanField(default=False)
    monto = models.DecimalField(max_digits=14, decimal_places=2, blank=True, default=0)
    impuesto = models.DecimalField(max_digits=14, decimal_places=2, blank=True, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, default=0)
    metodo_pago = models.CharField(max_length=50,blank=True,)  
    datos_transaccion = models.TextField(blank=True,default='')    
    fecha_pago = models.DateTimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Impresion, self).save(*args, **kwargs)    
    class Meta:
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(check=models.Q(monto__gte=0), name="impresion_monto_nonnegative"),
            models.CheckConstraint(check=models.Q(impuesto__gte=0), name="impresion_impuesto_nonnegative"),
            models.CheckConstraint(check=models.Q(total__gte=0), name="impresion_total_nonnegative"),
        ]


#bingo 75
class Carton75(models.Model):
    l1_1 = models.CharField(max_length=2, blank=True)  
    l1_2 = models.CharField(max_length=2, blank=True)  
    l1_3 = models.CharField(max_length=2, blank=True)  
    l1_4 = models.CharField(max_length=2, blank=True)  
    l1_5 = models.CharField(max_length=2, blank=True)  
    l2_1 = models.CharField(max_length=2, blank=True)  
    l2_2 = models.CharField(max_length=2, blank=True)  
    l2_3 = models.CharField(max_length=2, blank=True)  
    l2_4 = models.CharField(max_length=2, blank=True)  
    l2_5 = models.CharField(max_length=2, blank=True)  
    l3_1 = models.CharField(max_length=2, blank=True)  
    l3_2 = models.CharField(max_length=2, blank=True)  
    l3_3 = models.CharField(max_length=2, blank=True)  
    l3_4 = models.CharField(max_length=2, blank=True)  
    l3_5 = models.CharField(max_length=2, blank=True)  
    l4_1 = models.CharField(max_length=2, blank=True)  
    l4_2 = models.CharField(max_length=2, blank=True)  
    l4_3 = models.CharField(max_length=2, blank=True)  
    l4_4 = models.CharField(max_length=2, blank=True)  
    l4_5 = models.CharField(max_length=2, blank=True)  
    l5_1 = models.CharField(max_length=2, blank=True)  
    l5_2 = models.CharField(max_length=2, blank=True)  
    l5_3 = models.CharField(max_length=2, blank=True)  
    l5_4 = models.CharField(max_length=2, blank=True)  
    l5_5 = models.CharField(max_length=2, blank=True)  

class CabezeraImpre75(models.Model):
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida75, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuenta = models.CharField(max_length=30,blank=True)  
    banco = models.CharField(max_length=50, blank=True)  
    referencia = models.CharField(max_length=20, blank=True)  
    cantidad = models.PositiveIntegerField(default=0)  
    file = models.ImageField(upload_to = 'captures_bancos/')
    verficado = models.BooleanField(default=False)    


class Impresion75(models.Model):
    propietario = models.ForeignKey(CabezeraImpre75, on_delete=models.CASCADE)
    ganador_1 = models.BooleanField(default=False)
    posible_1 = models.BooleanField(default=False)
    ganador_2 = models.BooleanField(default=False)
    posible_2 = models.BooleanField(default=False)
    ganador_3 = models.BooleanField(default=False)
    posible_3 = models.BooleanField(default=False)
    ganador_4 = models.BooleanField(default=False)
    posible_4 = models.BooleanField(default=False)
    ganador_5 = models.BooleanField(default=False)
    posible_5 = models.BooleanField(default=False)
    ganador_6 = models.BooleanField(default=False)
    posible_6 = models.BooleanField(default=False)
    ganador_7 = models.BooleanField(default=False)
    posible_7 = models.BooleanField(default=False)
    ganador_8 = models.BooleanField(default=False)
    posible_8 = models.BooleanField(default=False)
    linea = models.IntegerField(default = 0)
    ganador_9 = models.BooleanField(default=False)
    posible_9 = models.BooleanField(default=False)
    ganador_10 = models.BooleanField(default=False)
    posible_10 = models.BooleanField(default=False)
    ganador = models.BooleanField(default=False)
    ganador_at = models.DateTimeField(blank=False, null=True)
    carton = models.ForeignKey(Carton75,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False,blank=False, null=True)
    enJuego = models.BooleanField(default=False)
    pago = models.BooleanField(default=False)
    monto = models.DecimalField(max_digits=14, decimal_places=2, blank=True, default=0)
    impuesto = models.DecimalField(max_digits=14, decimal_places=2, blank=True, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, default=0)
    metodo_pago = models.CharField(max_length=50,blank=True,)  
    datos_transaccion = models.TextField(blank=True,default='')    
    fecha_pago = models.DateTimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Impresion75, self).save(*args, **kwargs)    
    class Meta:
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(check=models.Q(monto__gte=0), name="impresion75_monto_nonnegative"),
            models.CheckConstraint(check=models.Q(impuesto__gte=0), name="impresion75_impuesto_nonnegative"),
            models.CheckConstraint(check=models.Q(total__gte=0), name="impresion75_total_nonnegative"),
        ]
