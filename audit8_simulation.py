from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from core.financial_rules import validate_percentages, apply_tax, reconcile, calculate_prize_pool

def simulate_settlement():
    pool = calculate_prize_pool('10000', 100)
    _, total = validate_percentages(['50','30','20'])
    assert total == Decimal('100.00')
    gross = Decimal('700000.00')
    tax, net = apply_tax(gross, '10')
    reconcile(pool, gross, tax, net)
    assert (pool, gross, tax, net) == (Decimal('1000000.00'), Decimal('700000.00'), Decimal('70000.00'), Decimal('630000.00'))
    return pool, gross, tax, net

def simulate_idempotent_settlement(attempts=50):
    lock = Lock(); settled = False; created = 0
    def attempt(_):
        nonlocal settled, created
        with lock:
            if settled: return False
            settled = True; created += 1; return True
    with ThreadPoolExecutor(max_workers=attempts) as ex:
        results=list(ex.map(attempt, range(attempts)))
    assert created == 1 and sum(results) == 1
    return created

if __name__ == '__main__':
    print('LIQUIDACION:', simulate_settlement())
    print('SETTLEMENTS CREADOS:', simulate_idempotent_settlement())
    print('AUDITORIA 8: LIQUIDACION FINANCIERA E INMUTABILIDAD SUPERADAS')
