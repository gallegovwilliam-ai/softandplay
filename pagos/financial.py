from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from django.db import transaction
from django.http import Http404
from django.utils import timezone

from cards.models import Impresion, Impresion75
from .models import PaymentRecord, PaymentRecord75
from core.models import AuditLog
from core.financial_ledger import ledger_entry
from core.financial_rules import money

CENT = Decimal('0.01')

def client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    return forwarded.split(',')[0].strip() if forwarded else request.META.get('REMOTE_ADDR')

def _payment(carton, user, method, reference, is75=False, request=None):
    if not carton.ganador:
        raise ValueError('El cartón no está marcado como ganador')
    Model = PaymentRecord75 if is75 else PaymentRecord
    with transaction.atomic():
        carton = type(carton).objects.select_for_update().get(pk=carton.pk)
        amount = money(carton.monto)
        tax = money(carton.impuesto)
        net = money(carton.total)
        if amount < 0 or tax < 0 or net < 0:
            raise ValueError('Los valores del premio no pueden ser negativos')
        if tax > amount or net > amount:
            raise ValueError('Los valores financieros del premio son inconsistentes')
        existing = Model.objects.filter(carton=carton).first()
        if carton.pago and existing is None:
            raise ValueError('Inconsistencia financiera: el cartón figura como pagado pero no existe PaymentRecord')
        if existing is not None:
            if existing.status == Model.STATUS_APPROVED:
                return existing, False
            if existing.status == Model.STATUS_VOID:
                raise ValueError('El pago fue anulado; requiere un nuevo proceso de pago')
            # Un registro pendiente/rechazado puede ser procesado explícitamente.
        if not method or len(method) > 50:
            raise ValueError('Método de pago inválido')
        if len(reference) > 100:
            raise ValueError('Referencia de transacción inválida')
        record, created = Model.objects.get_or_create(
            carton=carton,
            defaults={
                'processed_by': user,
                'status': Model.STATUS_APPROVED,
                'amount': amount,
                'tax': tax,
                'net_amount': net,
                'method': method,
                'transaction_reference': reference,
                'approved_at': timezone.now(),
                'currency': 'COP',
            },
        )
        if not created and record.status == Model.STATUS_APPROVED:
            return record, False
        record.processed_by = user
        record.status = Model.STATUS_APPROVED
        record.amount = amount
        record.tax = tax
        record.net_amount = net
        record.method = method
        record.transaction_reference = reference
        record.currency = 'COP'
        record.approved_at = timezone.now()
        record.save(update_fields=['processed_by','status','amount','tax','net_amount','method','transaction_reference','currency','approved_at'])
        carton.pago = True
        carton.monto = amount
        carton.impuesto = tax
        carton.total = net
        carton.metodo_pago = method
        carton.datos_transaccion = reference
        carton.fecha_pago = timezone.now()
        carton.save(update_fields=['pago', 'monto', 'impuesto', 'total', 'metodo_pago', 'datos_transaccion', 'fecha_pago'])
        AuditLog.objects.create(
            actor=user,
            action='PAGO_APROBADO_75' if is75 else 'PAGO_APROBADO',
            target_type='Impresion75' if is75 else 'Impresion',
            target_id=str(carton.pk),
            metadata='amount={};tax={};net={};method={};reference={}'.format(amount, tax, net, method, reference),
            ip_address=client_ip(request) if request else None,
        )
        # El pago genera un asiento de débito independiente del premio. La
        # clave hace la operación idempotente frente a reintentos.
        ledger_entry(
            user=user,
            entry_type='DEBITO',
            amount=net,
            reference_type='PaymentRecord75' if is75 else 'PaymentRecord',
            reference_id=record.pk,
            description='Pago de premio',
            request=request,
            unique_key='PAGO:{}:{}'.format('75' if is75 else '4', carton.pk),
        )
        return record, True
