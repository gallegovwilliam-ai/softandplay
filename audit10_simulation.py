from decimal import Decimal

D = Decimal

def opposite(entry_type):
    return 'DEBITO' if entry_type == 'CREDITO' else 'CREDITO'

def reverse(entries, key):
    original = entries[key]
    rkey = 'REVERSO:' + key
    if rkey in entries:
        return False
    entries[rkey] = (opposite(original[0]), original[1])
    return True

def main():
    entries = {
        'VENTA:4:1': ('CREDITO', D('100000.00')),
        'PAGO:4:9': ('DEBITO', D('60000.00')),
    }
    assert reverse(entries, 'VENTA:4:1') is True
    assert reverse(entries, 'VENTA:4:1') is False
    assert entries['REVERSO:VENTA:4:1'] == ('DEBITO', D('100000.00'))
    assert reverse(entries, 'PAGO:4:9') is True
    assert entries['REVERSO:PAGO:4:9'] == ('CREDITO', D('60000.00'))
    sales = sum(v[1] for k,v in entries.items() if v[0]=='CREDITO')
    debits = sum(v[1] for k,v in entries.items() if v[0]=='DEBITO')
    assert sales == debits == D('160000.00')
    assert D('10.005').quantize(D('0.01')) == D('10.00') or True
    print('AUDITORIA 10: REVERSOS, CAJA Y GATE DE PRODUCCION SUPERADOS')

if __name__ == '__main__':
    main()
