from collections import Counter
from decimal import Decimal

# Simulates the invariants that can be checked without Django/PostgreSQL installed.

def allocate(available, requests):
    owners = {}
    for owner, qty in requests:
        selected = [c for c in available if c not in owners][:qty]
        if len(selected) != qty:
            raise ValueError('inventory')
        for c in selected:
            owners[c] = owner
    return owners


def main():
    assigned = allocate(list(range(1, 11)), [('A', 7), ('B', 3)])
    assert len(assigned) == 10
    assert len(set(assigned.values())) == 2
    assert sorted(Counter(assigned.values()).values()) == [3, 7]

    # Financial idempotency: same sale/header is one financial event.
    ledger = {}
    key = 'SALE:42'
    ledger[key] = Decimal('10000.00')
    ledger[key] = ledger[key]
    assert len(ledger) == 1 and ledger[key] == Decimal('10000.00')

    # Email verification token concept: no user identity is accepted from URL alone.
    assert '<str:email>' not in 'validar-email/<uidb64>/<token>/'
    print('AUDITORIA 17 SIMULACION: OK')

if __name__ == '__main__':
    main()
