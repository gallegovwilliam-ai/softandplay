"""Reglas financieras deterministas para premios y conciliación.

Este módulo no realiza escrituras en base de datos. Su objetivo es que las
reglas monetarias puedan probarse de forma aislada antes de integrarlas con
Django.
"""
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

CENT = Decimal('0.01')
ZERO = Decimal('0.00')


def money(value):
    try:
        return Decimal(str(value or '0')).quantize(CENT, rounding=ROUND_HALF_UP)
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError('Monto monetario inválido')


def validate_percentages(percentages):
    vals = [money(p) for p in percentages]
    if any(p < ZERO or p > Decimal('100.00') for p in vals):
        raise ValueError('Cada porcentaje debe estar entre 0 y 100')
    total = sum(vals, ZERO)
    if total > Decimal('100.00'):
        raise ValueError('La suma de porcentajes de premio no puede superar 100%')
    return vals, total


def calculate_prize_pool(card_price, sold_cards):
    price = money(card_price)
    if price < ZERO:
        raise ValueError('El precio del cartón no puede ser negativo')
    if int(sold_cards) < 0:
        raise ValueError('La cantidad de cartones no puede ser negativa')
    return (price * int(sold_cards)).quantize(CENT, rounding=ROUND_HALF_UP)


def split_prize_pool(pool, winners_by_pattern):
    """Divide el pozo por patrón y ganador.

    winners_by_pattern es una secuencia de tuplas (porcentaje, cantidad_ganadores)
    y devuelve el premio total por ganador de un cartón que tenga esos patrones.
    Cada componente se redondea a centavos, igual que el sistema actual.
    """
    pool = money(pool)
    if pool < ZERO:
        raise ValueError('El pozo no puede ser negativo')
    percentages, _ = validate_percentages([p for p, _ in winners_by_pattern])
    total = ZERO
    components = []
    for pct, (_, count) in zip(percentages, winners_by_pattern):
        count = int(count)
        if count <= 0:
            raise ValueError('La cantidad de ganadores debe ser positiva')
        component = ((pool * pct / Decimal('100')) / Decimal(count)).quantize(CENT, rounding=ROUND_HALF_UP)
        components.append(component)
        total += component
    return total.quantize(CENT, rounding=ROUND_HALF_UP), components


def apply_tax(gross, tax_percent):
    gross = money(gross)
    tax_percent = money(tax_percent)
    if gross < ZERO:
        raise ValueError('El premio bruto no puede ser negativo')
    if tax_percent < ZERO or tax_percent > Decimal('100.00'):
        raise ValueError('El impuesto debe estar entre 0 y 100%')
    tax = (gross * tax_percent / Decimal('100')).quantize(CENT, rounding=ROUND_HALF_UP)
    net = (gross - tax).quantize(CENT, rounding=ROUND_HALF_UP)
    return tax, net


def reconcile(pool, prize_gross, tax, net):
    """Comprueba que una operación financiera cierre exactamente a centavos."""
    pool, prize_gross, tax, net = map(money, (pool, prize_gross, tax, net))
    if any(v < ZERO for v in (pool, prize_gross, tax, net)):
        raise ValueError('La conciliación no acepta valores negativos')
    if (prize_gross - tax) != net:
        raise ValueError('Premio bruto - impuesto no coincide con el neto')
    if prize_gross > pool:
        raise ValueError('El premio no puede superar el pozo')
    return True
