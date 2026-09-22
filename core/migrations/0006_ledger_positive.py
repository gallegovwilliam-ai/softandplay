from django.db import migrations, models
from django.db.models import Q

class Migration(migrations.Migration):
    dependencies = [('core','0005_remove_legacy_settlements')]
    operations = [migrations.AddConstraint(model_name='financialledger', constraint=models.CheckConstraint(check=Q(amount__gt=0), name='ledger_amount_positive'))]
