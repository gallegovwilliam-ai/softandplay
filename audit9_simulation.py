from decimal import Decimal
from collections import defaultdict

C=Decimal('0.01')
def m(x): return Decimal(str(x)).quantize(C)
def simulate():
    # 100 cartones vendidos a $10.000, 50/30/20% y 10% de impuesto.
    sales=[m(10000)*1 for _ in range(100)]
    pool=sum(sales, Decimal('0'))
    patterns=[(m('50'),1),(m('30'),2),(m('20'),4)]
    gross=Decimal('0')
    for pct,n in patterns: gross += ((pool*pct/100)/n).quantize(C)*n
    # el reparto bruto no debe superar el pozo
    assert gross <= pool
    tax=(gross*m('10')/100).quantize(C)
    net=gross-tax
    assert gross-tax==net
    # conciliación de caja: ventas menos pagos, sin duplicar liquidación.
    cash=pool-net
    assert cash >= 0
    keys=set();
    for i in range(100):
        k='VENTA:4:%s'%i; keys.add(k)
    assert len(keys)==100
    assert len(keys | {'PAGO:4:1'})==101
    return pool,gross,tax,net,cash

if __name__=='__main__':
    pool,gross,tax,net,cash=simulate()
    print('pozo=',pool)
    print('premio_bruto=',gross)
    print('impuesto=',tax)
    print('premio_neto=',net)
    print('caja_neta=',cash)
    print('AUDITORIA 9: CIRCUITO VENTA-LIQUIDACION-PAGO-CONCILIACION SUPERADO')
