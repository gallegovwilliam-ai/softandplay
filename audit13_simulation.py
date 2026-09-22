from decimal import Decimal

CENT = Decimal('0.01')


def wallet_move(balance, amount):
    amount = Decimal(str(amount)).quantize(CENT)
    if amount == 0:
        raise ValueError('zero')
    new_balance = balance + amount
    if new_balance < 0:
        raise ValueError('insufficient')
    tx_amount = abs(amount)
    direction = 'CREDITO' if amount > 0 else 'DEBITO'
    return new_balance, tx_amount, direction


def main():
    balance = Decimal('100.00')
    balance, tx, direction = wallet_move(balance, '-25.50')
    assert balance == Decimal('74.50')
    assert tx == Decimal('25.50') and direction == 'DEBITO'
    balance, tx, direction = wallet_move(balance, '10')
    assert balance == Decimal('84.50')
    assert tx == Decimal('10.00') and direction == 'CREDITO'
    print('Audit 13 simulation OK: wallet signed movements preserved with positive transaction amount.')


if __name__ == '__main__':
    main()
