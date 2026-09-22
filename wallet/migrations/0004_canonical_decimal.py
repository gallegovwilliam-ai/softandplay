from django.db import migrations, models
from decimal import Decimal

def copy_shadow(apps, schema_editor):
    Wallet=apps.get_model('wallet','Wallet')
    Tx=apps.get_model('wallet','TransactionWallet')
    for w in Wallet.objects.all():
        value=getattr(w,'balance_decimal',None)
        if value is None: value=Decimal(str(w.balance or 0))
        Wallet.objects.filter(pk=w.pk).update(balance=Decimal(str(value)).quantize(Decimal('0.01')))
    for t in Tx.objects.all():
        value=getattr(t,'amount_decimal',None)
        if value is None: value=Decimal(str(t.amount or 0))
        Tx.objects.filter(pk=t.pk).update(amount=Decimal(str(value)).quantize(Decimal('0.01')))

class Migration(migrations.Migration):
 dependencies=[('wallet','0003_wallet_nonnegative')]
 operations=[
  migrations.RunPython(copy_shadow,migrations.RunPython.noop),
  migrations.AlterField('wallet','balance',models.DecimalField(max_digits=14,decimal_places=2,default=Decimal('10.00'))),
  migrations.RemoveConstraint('wallet','wallet_balance_decimal_nonnegative'),
  migrations.AddConstraint('wallet',models.CheckConstraint(check=models.Q(balance__gte=0), name='wallet_balance_nonnegative')),
  migrations.AlterField('transactionwallet','amount',models.DecimalField(max_digits=14,decimal_places=2)),
  migrations.RemoveField('wallet','balance_decimal'),
  migrations.RemoveField('transactionwallet','amount_decimal'),
 ]
