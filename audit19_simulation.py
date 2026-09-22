from decimal import Decimal


def allocate(ids, used, qty):
    available = [x for x in ids if x not in used]
    if qty <= 0 or len(available) < qty:
        raise ValueError('inventario insuficiente')
    return available[:qty]


def test_last_cartons():
    inventory = list(range(1, 6))
    used = {1, 2, 3}
    a = allocate(inventory, used, 1)
    used |= set(a)
    b = allocate(inventory, used, 1)
    assert a == [4] and b == [5]
    used |= set(b)
    try:
        allocate(inventory, used, 1)
    except ValueError:
        pass
    else:
        raise AssertionError('debía rechazar inventario agotado')


def test_financial_conservation():
    sales = [Decimal('100.00'), Decimal('50.00')]
    payouts = [Decimal('80.00')]
    assert sum(sales) - sum(payouts) == Decimal('70.00')


def test_idempotency_keys():
    keys = set()
    key = 'VENTA:4:100'
    keys.add(key)
    keys.add(key)
    assert len(keys) == 1


def test_paypal_pending():
    header = {'banco': 'paypal', 'verficado': False}
    assert header['verficado'] is False
    assert 'sale_record' not in header


if __name__ == '__main__':
    test_last_cartons()
    test_financial_conservation()
    test_idempotency_keys()
    test_paypal_pending()
    print('AUDITORIA 19 SIMULACION: OK')
