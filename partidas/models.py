from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
# A new user has registered.


class Partida(models.Model):
    fecha = models.DateField()
    partida = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=200, blank=True)  
    figura_1 = models.BooleanField(default=False)
    ganador_1 = models.BooleanField(default=False)
    monto_1 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_2 = models.BooleanField(default=False)
    ganador_2 = models.BooleanField(default=False)
    monto_2 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_3 = models.BooleanField(default=False)
    ganador_3 = models.BooleanField(default=False)
    monto_3 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_4 = models.BooleanField(default=False)
    ganador_4 = models.BooleanField(default=False)
    monto_4 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_5 = models.BooleanField(default=False)
    ganador_5 = models.BooleanField(default=False)
    monto_5 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_5 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_6 = models.BooleanField(default=False)
    ganador_6 = models.BooleanField(default=False)
    monto_6 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_6 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_7 = models.BooleanField(default=False)
    ganador_7 = models.BooleanField(default=False)
    monto_7 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_7 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_8 = models.BooleanField(default=False)
    ganador_8 = models.BooleanField(default=False)
    monto_8 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_8 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_9 = models.BooleanField(default=False)
    ganador_9 = models.BooleanField(default=False)
    monto_9 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_9 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_10 = models.BooleanField(default=False)
    ganador_10 = models.BooleanField(default=False)
    monto_10 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_10 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    monto_carton = models.DecimalField(max_digits=14, decimal_places=2,  default=0)
    cartones_vendidos = models.PositiveIntegerField(default=0)  
    monto_acumulado = models.DecimalField(max_digits=14, decimal_places=2,  default=0)
    impuesto = models.DecimalField(max_digits=14, decimal_places=2,  default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2,  default=0)
    termino = models.BooleanField(default=False)
    inicio = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False,blank=False, null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Partida, self).save(*args, **kwargs)    
    def __str__(self):
        return  "Partida Loteria Mexicana #" + str(self.partida) + " / " + str(self.fecha) + " / " + self.descripcion
    class Meta:
        ordering = ['id']
        constraints = [models.UniqueConstraint(fields=['fecha', 'partida'], name='uniq_partida_fecha_num')] + [models.CheckConstraint(check=models.Q(**{f'{n}__gte': 0}), name=f'partida_{n}_nonnegative') for n in ['monto_1','monto_2','monto_3','monto_4','monto_5','monto_6','monto_7','monto_8','monto_9','monto_10','monto_carton','monto_acumulado','impuesto','total']] + [models.CheckConstraint(check=models.Q(**{f'{n}__gte': 0}) & models.Q(**{f'{n}__lte': 100}), name=f'partida_{n}_range') for n in ['porciento_1','porciento_2','porciento_3','porciento_4','porciento_5','porciento_6','porciento_7','porciento_8','porciento_9','porciento_10']]
        


class PartidaSequence(models.Model):
    TIPO_LOTERIA = 'LOTO'
    TIPO_BINGO75 = 'BINGO75'
    TIPO_CHOICES = ((TIPO_LOTERIA, 'Lotería Mexicana'), (TIPO_BINGO75, 'Bingo 75'))
    fecha = models.DateField(unique=False)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    ultimo_numero = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['fecha', 'tipo'], name='uniq_partida_sequence_fecha_tipo')]

    def __str__(self):
        return '{} {} #{}'.format(self.fecha, self.tipo, self.ultimo_numero)

class Jugada(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    balota = models.CharField(max_length=2, blank=True)
    orden = models.CharField(max_length=2, blank=True)
    created_at = models.DateTimeField(editable=False,blank=False, null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Jugada, self).save(*args, **kwargs)    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['partida', 'balota'], name='uniq_jugada_partida_balota')]

 #BINGO
 
class Partida75(models.Model):
    fecha = models.DateField()
    partida = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=200, blank=True)  
    figura_1 = models.BooleanField(default=False)
    ganador_1 = models.BooleanField(default=False)
    monto_1 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_2 = models.BooleanField(default=False)
    ganador_2 = models.BooleanField(default=False)
    monto_2 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_3 = models.BooleanField(default=False)
    ganador_3 = models.BooleanField(default=False)
    monto_3 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_4 = models.BooleanField(default=False)
    ganador_4 = models.BooleanField(default=False)
    monto_4 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_5 = models.BooleanField(default=False)
    ganador_5 = models.BooleanField(default=False)
    monto_5 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_5 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_6 = models.BooleanField(default=False)
    ganador_6 = models.BooleanField(default=False)
    monto_6 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_6 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_7 = models.BooleanField(default=False)
    ganador_7 = models.BooleanField(default=False)
    monto_7 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_7 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_8 = models.BooleanField(default=False)
    ganador_8 = models.BooleanField(default=False)
    monto_8 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_8 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_9 = models.BooleanField(default=False)
    ganador_9 = models.BooleanField(default=False)
    monto_9 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_9 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    figura_10 = models.BooleanField(default=False)
    ganador_10 = models.BooleanField(default=False)
    monto_10 = models.DecimalField(max_digits=14, decimal_places=2,  blank=True,default=0)
    porciento_10 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)  
    cartones_vendidos = models.PositiveIntegerField(default=0)  
    termino = models.BooleanField(default=False)
    inicio = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False,blank=False, null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Partida75, self).save(*args, **kwargs)    
    def __str__(self):
        return  "Partida Bingo 75 #" + str(self.partida) + " / " + str(self.fecha) + " / " + self.descripcion
    monto_carton = models.DecimalField(max_digits=14, decimal_places=2, blank=True, default=0)
  class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['fecha', 'partida'], name='uniq_partida75_fecha_num')
        ] + [
            models.CheckConstraint(check=models.Q(**{f'{n}__gte': 0}), name=f'partida75_{n}_nonnegative') 
            for n in ['monto_1','monto_2','monto_3','monto_4','monto_5','monto_6','monto_7','monto_8','monto_9','monto_10','monto_carton']
        ] + [
            models.CheckConstraint(check=models.Q(**{f'{n}__gte': 0}) & models.Q(**{f'{n}__lte': 100}), name=f'partida75_{n}_range') 
            for n in ['porciento_1','porciento_2','porciento_3','porciento_4','porciento_5','porciento_6','porciento_7','porciento_8','porciento_9','porciento_10']
        ]


class Jugada75(models.Model):
    partida = models.ForeignKey(Partida75, on_delete=models.CASCADE)
    balota = models.CharField(max_length=2, blank=True)
    orden = models.CharField(max_length=2, blank=True)
    created_at = models.DateTimeField(editable=False, blank=False, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Jugada75, self).save(*args, **kwargs)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['partida', 'balota'], name='uniq_jugada75_partida_balota')]
