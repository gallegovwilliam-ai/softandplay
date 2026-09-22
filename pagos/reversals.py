from django.db import transaction
from django.utils import timezone
from core.models import FinancialLedger, AuditLog
from core.financial_ledger import ledger_entry
from .models import SaleRecord, SaleRecord75, PaymentRecord, PaymentRecord75, FinancialReversal


def reverse_ledger(original, user, request=None, reason=''):
    """Create one compensating ledger entry; never edits/deletes the original."""
    if original.entry_type == FinancialLedger.ENTRY_CREDIT:
        opposite = FinancialLedger.ENTRY_DEBIT
    else:
        opposite = FinancialLedger.ENTRY_CREDIT
    key = 'REVERSO:{}'.format(original.unique_key)
    entry, created = ledger_entry(
        user=user,
        entry_type=opposite,
        amount=original.amount,
        reference_type='Reversal',
        reference_id=original.pk,
        description=('Reverso: ' + (reason or original.description))[:255],
        request=request,
        currency=original.currency,
        unique_key=key,
    )
    return entry, created


def void_sale(sale, user, request=None, reason=''):
    Sale = SaleRecord75 if isinstance(sale, SaleRecord75) else SaleRecord
    with transaction.atomic():
        sale = Sale.objects.select_for_update().get(pk=sale.pk)
        if sale.status == Sale.STATUS_VOID:
            return sale, False
        if sale.status != Sale.STATUS_APPROVED:
            raise ValueError('Solo una venta aprobada puede anularse')
        ref_type = 'SaleRecord75' if Sale is SaleRecord75 else 'SaleRecord'
        original = FinancialLedger.objects.select_for_update().get(unique_key='VENTA:{}:{}'.format('75' if Sale is SaleRecord75 else '4', sale.pk))
        reversal, created = reverse_ledger(original, user, request, reason or 'Anulación de venta')
        if created:
            FinancialReversal.objects.create(original_entry=original, reversal_entry=reversal, created_by=user, reason=(reason or 'Anulación de venta')[:255])
        sale.status = Sale.STATUS_VOID
        sale.save(update_fields=['status'])
        AuditLog.objects.create(actor=user, action='VENTA_ANULADA', target_type=ref_type, target_id=str(sale.pk), metadata='reason={}'.format(reason[:1000]), ip_address=request.META.get('REMOTE_ADDR') if request else None)
        return sale, True


def void_payment(payment, user, request=None, reason=''):
    Payment = PaymentRecord75 if isinstance(payment, PaymentRecord75) else PaymentRecord
    with transaction.atomic():
        payment = Payment.objects.select_for_update().get(pk=payment.pk)
        if payment.status == Payment.STATUS_VOID:
            return payment, False
        if payment.status != Payment.STATUS_APPROVED:
            raise ValueError('Solo un pago aprobado puede anularse')
        key = 'PAGO:{}:{}'.format('75' if Payment is PaymentRecord75 else '4', payment.carton_id)
        original = FinancialLedger.objects.select_for_update().get(unique_key=key)
        reversal, created = reverse_ledger(original, user, request, reason or 'Reverso de pago de premio')
        if created:
            FinancialReversal.objects.create(original_entry=original, reversal_entry=reversal, created_by=user, reason=(reason or 'Reverso de pago de premio')[:255])
        payment.status = Payment.STATUS_VOID
        payment.save(update_fields=['status'])
        payment.carton.pago = False
        payment.carton.save(update_fields=['pago'])
        AuditLog.objects.create(actor=user, action='PAGO_ANULADO', target_type='PaymentRecord75' if Payment is PaymentRecord75 else 'PaymentRecord', target_id=str(payment.pk), metadata='reason={}'.format(reason[:1000]), ip_address=request.META.get('REMOTE_ADDR') if request else None)
        return payment, True
