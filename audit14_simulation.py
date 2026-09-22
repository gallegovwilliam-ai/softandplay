from decimal import Decimal


def wallet_move(balance, amount):
    amount = Decimal(str(amount)).quantize(Decimal('0.01'))
    if amount == 0:
        raise ValueError('zero')
    new_balance = balance + amount
    if new_balance < 0:
        raise ValueError('insufficient')
    return new_balance, abs(amount), 'CREDITO' if amount > 0 else 'DEBITO'


def paypal_request(reference, verified_externally):
    # El navegador puede enviar una referencia, pero no puede convertirla en pago aprobado.
    return 'APROBADO' if verified_externally else 'PENDIENTE'


assert wallet_move(Decimal('100.00'), '-25.50') == (Decimal('74.50'), Decimal('25.50'), 'DEBITO')
assert wallet_move(Decimal('74.50'), '10.00') == (Decimal('84.50'), Decimal('10.00'), 'CREDITO')
assert paypal_request('FAKE-123', False) == 'PENDIENTE'
assert paypal_request('PAY-123', True) == 'APROBADO'
print('AUDITORIA 14 SIMULACION: OK')
