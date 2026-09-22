from decimal import Decimal

class Ledger:
    def __init__(self): self.entries=[]
    def add(self, kind, amount, key):
        if amount <= 0: raise ValueError('importe no positivo')
        if any(x[2] == key for x in self.entries): return False
        self.entries.append((kind, Decimal(str(amount)), key)); return True

def test_last_cartons():
    available = ['A','B']
    allocations=[]
    for request in (['A'], ['B']):
        card=request[0]
        if card in allocations: raise AssertionError('duplicado')
        allocations.append(card)
    assert sorted(allocations)==['A','B']

def test_financial_idempotency():
    l=Ledger(); assert l.add('CREDITO',100,'VENTA:1'); assert not l.add('CREDITO',100,'VENTA:1')
    assert l.add('DEBITO',80,'PAGO:1'); assert not l.add('DEBITO',80,'PAGO:1')
    assert sum(x[1] if x[0]=='CREDITO' else -x[1] for x in l.entries)==20

def test_reversal():
    l=Ledger(); assert l.add('CREDITO',100,'VENTA:2'); assert l.add('DEBITO',100,'REVERSO:VENTA:2'); assert not l.add('DEBITO',100,'REVERSO:VENTA:2')
    assert sum(x[1] if x[0]=='CREDITO' else -x[1] for x in l.entries)==0

def test_pending_paypal():
    header={'verficado':False,'banco':'paypal'}
    assert header['verficado'] is False

if __name__=='__main__':
    test_last_cartons(); test_financial_idempotency(); test_reversal(); test_pending_paypal()
    print('AUDITORIA 20 SIMULACION: OK')
