from decimal import Decimal
from core.financial_rules import money, calculate_prize_pool, validate_percentages, apply_tax, reconcile


def main():
    price = money('10000')
    pool = calculate_prize_pool(price, 100)
    validate_percentages([50, 30, 20])
    tax, net = apply_tax(Decimal('700000'), Decimal('10'))
    reconcile(pool, Decimal('700000'), tax, net)
    assert pool == Decimal('1000000.00')
    assert tax == Decimal('70000.00')
    assert net == Decimal('630000.00')
    for bad in ([101,0,0],[60,50,0],[-1,0,0]):
        try: validate_percentages(bad)
        except ValueError: pass
        else: raise AssertionError('Configuracion invalida aceptada')
    try: calculate_prize_pool(price, -1)
    except ValueError: pass
    else: raise AssertionError('Cantidad negativa aceptada')
    print('AUDITORIA 11: DECIMALES, REGLAS Y VALIDACIONES SUPERADAS')

if __name__ == '__main__': main()
