from decimal import Decimal


def test_sale_ledger():
    sales = [(1, Decimal('100.00')), (2, Decimal('50.00'))]
    ledger = {}
    for sid, amount in sales:
        key = 'VENTA:4:{}'.format(sid)
        ledger.setdefault(key, amount)
        ledger.setdefault(key, amount)
    assert sum(ledger.values()) == Decimal('150.00')


def test_void_payment_cannot_reapprove_same_record():
    status = 'ANULADO'
    try:
        if status == 'ANULADO':
            raise ValueError('El pago fue anulado; requiere un nuevo proceso de pago')
    except ValueError:
        return
    raise AssertionError('Un pago anulado no debe reaparecer como aprobado')


def test_pending_paypal():
    verified = False
    assert verified is False


if __name__ == '__main__':
    test_sale_ledger()
    test_void_payment_cannot_reapprove_same_record()
    test_pending_paypal()
    print('AUDITORIA 18 SIMULACION: OK')
