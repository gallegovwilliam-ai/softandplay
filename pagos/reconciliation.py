from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from cards.models import CabezeraImpre, CabezeraImpre75
from partidas.models import Partida, Partida75
from core.financial_ledger import ledger_entry
from core.financial_rules import money
from .models import SaleRecord, SaleRecord75


def _register(header, user, is75=False, request=None):
    Sale = SaleRecord75 if is75 else SaleRecord
    partida = (Partida75 if is75 else Partida).objects.select_for_update().get(pk=header.partida_id)
    if partida.inicio or partida.termino:
        raise ValueError('La venta no puede registrarse después de iniciar o terminar la partida')
    try:
        quantity = int(header.cantidad or 0)
    except (TypeError, ValueError):
        raise ValueError('Cantidad de cartones inválida')
    if quantity <= 0:
        raise ValueError('La cantidad de cartones debe ser positiva')
    price = money(getattr(partida, 'monto_carton', partida.monto_carton))
    amount = money(price * quantity)
    obj, created = Sale.objects.get_or_create(
        header=header,
        defaults={
            'processed_by': user,
            'status': Sale.STATUS_APPROVED,
            'quantity': quantity,
            'unit_price': price,
            'amount': amount,
            'currency': 'COP',
            'approved_at': timezone.now(),
        },
    )
    if not created:
        return obj, False
    ledger_entry(
        user=user,
        entry_type='CREDITO',
        amount=amount,
        reference_type='SaleRecord75' if is75 else 'SaleRecord',
        reference_id=obj.pk,
        description='Venta de cartones aprobada',
        request=request,
        unique_key='VENTA:{}:{}'.format('75' if is75 else '4', obj.pk),
    )
    return obj, True


def register_sale(header, user, request=None):
    with transaction.atomic():
        header = CabezeraImpre.objects.select_for_update().get(pk=header.pk)
        return _register(header, user, False, request)


def register_sale75(header, user, request=None):
    with transaction.atomic():
        header = CabezeraImpre75.objects.select_for_update().get(pk=header.pk)
        return _register(header, user, True, request)
