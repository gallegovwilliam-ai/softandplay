from django.db import models
from cards.models import Impresion, Impresion75, CabezeraImpre, CabezeraImpre75
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
# Create your models here.
import datetime

class MensajeCarton(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    carton = models.ForeignKey(Impresion, on_delete = models.CASCADE)
    mensaje = models.TextField()    
    created_at = models.DateTimeField(editable=False,default='2020-06-29')
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(MensajeCarton, self).save(*args, **kwargs)    

class MensajeCarton75(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    carton = models.ForeignKey(Impresion75, on_delete = models.CASCADE)
    mensaje = models.TextField()    
    created_at = models.DateTimeField(editable=False,default='2020-06-29')
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(MensajeCarton75, self).save(*args, **kwargs)    



class PaymentRecord(models.Model):
    STATUS_PENDING = 'PENDIENTE'
    STATUS_APPROVED = 'APROBADO'
    STATUS_REJECTED = 'RECHAZADO'
    STATUS_VOID = 'ANULADO'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_APPROVED, 'Aprobado'),
        (STATUS_REJECTED, 'Rechazado'),
        (STATUS_VOID, 'Anulado'),
    )
    carton = models.OneToOneField(Impresion, on_delete=models.PROTECT, related_name='payment_record')
    processed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='processed_payments')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    net_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='COP')
    method = models.CharField(max_length=50, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'Pago carton #{} {}'.format(self.carton_id, self.status)


class PaymentRecord75(models.Model):
    carton = models.OneToOneField(Impresion75, on_delete=models.PROTECT, related_name='payment_record')
    processed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='processed_payments75')
    status = models.CharField(max_length=12, choices=PaymentRecord.STATUS_CHOICES, default=PaymentRecord.STATUS_PENDING)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    net_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='COP')
    method = models.CharField(max_length=50, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'Pago bingo75 carton #{} {}'.format(self.carton_id, self.status)


class Settlement(models.Model):
    STATUS_SETTLED = 'LIQUIDADA'
    STATUS_CHOICES = ((STATUS_SETTLED, 'Liquidada'),)
    partida = models.OneToOneField('partidas.Partida', on_delete=models.PROTECT, related_name='settlement')
    settled_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='settlements')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_SETTLED)
    sold_cards = models.PositiveIntegerField(default=0)
    pool = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    prize_gross = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    prize_net = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    settled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-settled_at']

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError('La liquidación es inmutable')
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError('La liquidación es inmutable')

    def __str__(self):
        return 'Liquidación partida #{} {}'.format(self.partida_id, self.status)


class Settlement75(models.Model):
    STATUS_SETTLED = 'LIQUIDADA'
    STATUS_CHOICES = ((STATUS_SETTLED, 'Liquidada'),)
    partida = models.OneToOneField('partidas.Partida75', on_delete=models.PROTECT, related_name='settlement75')
    settled_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='settlements75')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_SETTLED)
    sold_cards = models.PositiveIntegerField(default=0)
    pool = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    prize_gross = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    prize_net = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    settled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-settled_at']

    def __str__(self):
        return 'Liquidación bingo75 #{} {}'.format(self.partida_id, self.status)


class SaleRecord(models.Model):
    STATUS_APPROVED = 'APROBADA'
    STATUS_VOID = 'ANULADA'
    STATUS_CHOICES = ((STATUS_APPROVED, 'Aprobada'), (STATUS_VOID, 'Anulada'))
    header = models.OneToOneField(CabezeraImpre, on_delete=models.PROTECT, related_name='sale_record')
    processed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales_recorded')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_APPROVED)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='COP')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class SaleRecord75(models.Model):
    STATUS_APPROVED = 'APROBADA'
    STATUS_VOID = 'ANULADA'
    STATUS_CHOICES = ((STATUS_APPROVED, 'Aprobada'), (STATUS_VOID, 'Anulada'))
    header = models.OneToOneField(CabezeraImpre75, on_delete=models.PROTECT, related_name='sale_record75')
    processed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales_recorded75')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_APPROVED)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='COP')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class CashReconciliation(models.Model):
    date = models.DateField(unique=True)
    sales = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    payouts = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    refunds = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    net_cash = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cash_reconciliations')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

class FinancialReversal(models.Model):
    original_entry = models.OneToOneField('core.FinancialLedger', on_delete=models.PROTECT, related_name='reversal')
    reversal_entry = models.OneToOneField('core.FinancialLedger', on_delete=models.PROTECT, related_name='reversal_of')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='financial_reversals')
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError('El reverso financiero es inmutable')
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError('El reverso financiero es inmutable')
