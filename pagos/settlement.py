from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.db import models
from cards.models import Impresion, Impresion75
from .models import SaleRecord, SaleRecord75
from partidas.models import Partida, Partida75
from configuracion.models import Config
from core.financial_rules import money, validate_percentages, apply_tax, reconcile
from .models import Settlement, Settlement75


def _settle(model, card_model, settlement_model, partida_id, user, is75=False, request=None):
    with transaction.atomic():
        partida = model.objects.select_for_update().get(pk=partida_id)
        existing = settlement_model.objects.select_for_update().filter(partida=partida).first()
        if existing:
            return existing, False
        if not partida.termino:
            raise ValueError('La partida debe estar terminada antes de liquidarla')
        config = Config.objects.get(pk=1)
        price = money(partida.monto_carton)
        Sale = SaleRecord75 if is75 else SaleRecord
        sold = Sale.objects.filter(header__partida=partida, status=Sale.STATUS_APPROVED).aggregate(total=models.Sum('quantity'))['total'] or 0
        sold = int(sold)
        pool = (price * sold).quantize(Decimal('0.01'))
        percentages = [money(getattr(partida, 'porciento_{}'.format(i))) for i in range(1,11)]
        validate_percentages(percentages)
        tax_pct = money(config.impuesto)
        total_gross = Decimal('0.00')
        total_tax = Decimal('0.00')
        total_net = Decimal('0.00')
        winners = card_model.objects.select_for_update().filter(propietario__partida=partida, propietario__verficado=True, ganador=True)
        counts = {i: card_model.objects.filter(propietario__partida=partida, propietario__verficado=True, **{'ganador_{}'.format(i): True}).count() for i in range(1,11)}
        for carton in winners: 
            gross = Decimal('0.00')
            for i in range(1,11):
                if getattr(carton, 'ganador_{}'.format(i), False) and counts[i] > 0:
                    pct = percentages[i-1]
                    gross += ((pool * pct / Decimal('100')) / Decimal(counts[i])).quantize(Decimal('0.01'))
            tax, net = apply_tax(gross, tax_pct)
            carton.monto = gross
            carton.impuesto = tax
            carton.total = net
            carton.save(update_fields=['monto','impuesto','total'])
            total_gross += gross
            total_tax += tax
            total_net += net
        total_tax = total_tax.quantize(Decimal('0.01'))
        total_net = total_net.quantize(Decimal('0.01'))
        reconcile(pool, total_gross, total_tax, total_net)
        partida.cartones_vendidos = sold
        partida.monto_acumulado = pool
        partida.impuesto = total_tax
        partida.total = total_net
        partida.save(update_fields=['cartones_vendidos','monto_acumulado','impuesto','total'])
        obj = settlement_model.objects.create(partida=partida, settled_by=user, status=settlement_model.STATUS_SETTLED, sold_cards=sold, pool=pool, prize_gross=total_gross, tax=total_tax, prize_net=total_net)
        return obj, True


def settle_partida(partida_id, user, request=None):
    return _settle(Partida, Impresion, Settlement, partida_id, user, False, request)

def settle_partida75(partida_id, user, request=None):
    return _settle(Partida75, Impresion75, Settlement75, partida_id, user, True, request)
