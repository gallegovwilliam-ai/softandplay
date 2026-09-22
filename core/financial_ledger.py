from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import FinancialLedger, AuditLog


def ledger_entry(*, user, entry_type, amount, reference_type, reference_id, description='', request=None, currency='COP', unique_key=''):
    amount = Decimal(str(amount)).quantize(Decimal('0.01'))
    if amount == 0:
        raise ValueError('Un movimiento financiero no puede tener valor cero')
    if not unique_key or not str(unique_key).strip():
        raise ValueError('Todo movimiento financiero debe tener una clave única')
    if entry_type not in (FinancialLedger.ENTRY_CREDIT, FinancialLedger.ENTRY_DEBIT):
        raise ValueError('Tipo de movimiento financiero inválido')
    ip = None
    if request is not None:
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
        ip = forwarded.split(',')[0].strip() if forwarded else request.META.get('REMOTE_ADDR')
    with transaction.atomic():
        obj, created = FinancialLedger.objects.get_or_create(
            unique_key=unique_key,
            defaults={
                'user': user,
                'entry_type': entry_type,
                'amount': amount,
                'currency': currency,
                'reference_type': reference_type,
                'reference_id': str(reference_id),
                'description': description[:255],
                'ip_address': ip,
            }
        )
        if created:
            AuditLog.objects.create(
                actor=user,
                action='MOVIMIENTO_FINANCIERO',
                target_type=reference_type,
                target_id=str(reference_id),
                metadata='type={};amount={};currency={};key={}'.format(entry_type, amount, currency, unique_key),
                ip_address=ip,
            )
        return obj, created
