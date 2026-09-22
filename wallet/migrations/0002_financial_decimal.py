from django.db import migrations, models
from decimal import Decimal


def copy_legacy_balances(apps, schema_editor):
    Wallet = apps.get_model('wallet', 'Wallet')
    TransactionWallet = apps.get_model('wallet', 'TransactionWallet')
    for w in Wallet.objects.all().iterator():
        w.balance_decimal = Decimal(str(w.balance or 0))
        w.save(update_fields=['balance_decimal'])
    for t in TransactionWallet.objects.all().iterator():
        t.amount_decimal = Decimal(str(t.amount or 0))
        t.save(update_fields=['amount_decimal'])

class Migration(migrations.Migration):
    dependencies = [('wallet', '0001_initial')]
    operations = [
        migrations.AddField('wallet', 'balance_decimal', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
        migrations.AddField('transactionwallet', 'amount_decimal', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
        migrations.RunPython(copy_legacy_balances, migrations.RunPython.noop),
    ]
