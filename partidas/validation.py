from decimal import Decimal, InvalidOperation
from core.financial_rules import money, validate_percentages


def validate_partida_post(data):
    try:
        price = money(data.get('monto_carton', '0'))
    except ValueError:
        raise ValueError('El precio del cartón no es válido')
    if price <= 0:
        raise ValueError('El precio del cartón debe ser mayor que cero')
    values=[]
    for i in range(1,11):
        try:
            values.append(Decimal(str(data.get('porciento_{}'.format(i), '0') or '0')))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError('Porcentaje inválido en la figura {}'.format(i))
    validate_percentages(values)
    return price, values
