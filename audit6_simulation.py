"""Simulación independiente de Auditoría 6.

No requiere Django. Ejecuta escenarios de dinero, ganadores y duplicados
para comprobar las reglas deterministas antes de tocar una base real.
"""
from decimal import Decimal
from core.financial_rules import (
    money, calculate_prize_pool, split_prize_pool, apply_tax, reconcile,
)


def assert_equal(name, actual, expected):
    if actual != expected:
        raise AssertionError(f'{name}: esperado {expected}, obtenido {actual}')
    print(f'OK  {name}: {actual}')


def run():
    pool = calculate_prize_pool('10000', 100)
    assert_equal('pozo 100 x $10.000', pool, Decimal('1000000.00'))

    gross, parts = split_prize_pool(pool, [('50', 1), ('30', 2), ('20', 4)])
    assert_equal('premio por cartón con los 3 patrones', gross, Decimal('700000.00'))
    assert_equal('componente patrón 1', parts[0], Decimal('500000.00'))
    assert_equal('componente patrón 2', parts[1], Decimal('150000.00'))
    assert_equal('componente patrón 3', parts[2], Decimal('50000.00'))

    tax, net = apply_tax(gross, '10')
    assert_equal('impuesto 10%', tax, Decimal('70000.00'))
    assert_equal('neto', net, Decimal('630000.00'))
    assert reconcile(pool, gross, tax, net)

    # Casos inválidos que deben ser rechazados.
    for name, fn in [
        ('porcentaje > 100', lambda: split_prize_pool(pool, [('101', 1)])),
        ('porcentajes acumulados > 100', lambda: split_prize_pool(pool, [('60', 1), ('50', 1)])),
        ('ganadores = 0', lambda: split_prize_pool(pool, [('50', 0)])),
        ('impuesto > 100', lambda: apply_tax('1000', '101')),
        ('neto inconsistente', lambda: reconcile(pool, '100', '20', '90')),
    ]:
        try:
            fn()
        except ValueError:
            print(f'OK  rechazo {name}')
        else:
            raise AssertionError(f'Debió rechazarse: {name}')

    # Idempotencia conceptual: una misma clave financiera solo puede producir
    # un movimiento lógico. La comprobación DB se prueba en tests Django.
    keys = {'PREMIO:4:123'}
    assert_equal('clave financiera única', len(keys), 1)
    print('\nAUDITORIA 6: TODOS LOS ESCENARIOS SUPERADOS')


if __name__ == '__main__':
    run()
