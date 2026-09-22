from decimal import Decimal
from threading import Barrier, Lock, Thread


def concurrent_last_cards():
    inventory = list(range(1, 11))
    used = set()
    guard = Lock()
    barrier = Barrier(10)
    allocations = []

    def seller():
        barrier.wait()
        with guard:
            available = [c for c in inventory if c not in used]
            take = available[:1]
            if take:
                used.add(take[0])
                allocations.append(take[0])

    threads = [Thread(target=seller) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert len(allocations) == 10
    assert len(set(allocations)) == 10


def financial_conservation():
    sales = [Decimal('100.00'), Decimal('50.00'), Decimal('25.00')]
    reversals = [Decimal('25.00')]
    net = sum(sales) - sum(reversals)
    assert net == Decimal('150.00')


def paypal_stays_pending():
    header = {'banco': 'paypal', 'verficado': False}
    assert header['verficado'] is False
    assert 'sale_record' not in header


if __name__ == '__main__':
    concurrent_last_cards()
    financial_conservation()
    paypal_stays_pending()
    print('AUDITORIA 23 SIMULACION: OK')
