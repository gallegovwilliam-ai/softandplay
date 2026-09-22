from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('wallet', '0004_canonical_decimal')]
    operations = [
        migrations.AddConstraint(
            'transactionwallet',
            models.CheckConstraint(check=models.Q(amount__gte=0), name='transactionwallet_amount_nonnegative'),
        ),
    ]
