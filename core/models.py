from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class AuditLog(models.Model):
    actor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='audit_events')
    action = models.CharField(max_length=80)
    target_type = models.CharField(max_length=80, blank=True)
    target_id = models.CharField(max_length=80, blank=True)
    metadata = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class FinancialLedger(models.Model):
    ENTRY_CREDIT = 'CREDITO'
    ENTRY_DEBIT = 'DEBITO'
    ENTRY_CHOICES = ((ENTRY_CREDIT, 'Crédito'), (ENTRY_DEBIT, 'Débito'))
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name='financial_entries')
    entry_type = models.CharField(max_length=10, choices=ENTRY_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3, default='COP')
    reference_type = models.CharField(max_length=80)
    reference_id = models.CharField(max_length=80)
    unique_key = models.CharField(max_length=160, unique=True)
    description = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError('FinancialLedger es inmutable y no admite modificaciones')
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError('FinancialLedger es inmutable y no admite eliminaciones')

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['reference_type', 'reference_id']), models.Index(fields=['user', 'created_at'])]
        constraints = [models.CheckConstraint(check=models.Q(amount__gt=0), name='ledger_amount_positive')]
