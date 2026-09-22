from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('wallet','0002_financial_decimal')]
    operations = [migrations.AddConstraint(model_name='wallet', constraint=models.CheckConstraint(check=models.Q(balance_decimal__gte=0), name='wallet_balance_decimal_nonnegative'))]
