from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [('pagos','0006_sales_reconciliation')]
    operations = [
        migrations.CreateModel(
            name='FinancialReversal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('original_entry', models.OneToOneField(on_delete=models.PROTECT, related_name='reversal', to='core.financialledger')),
                ('reversal_entry', models.OneToOneField(on_delete=models.PROTECT, related_name='reversal_of', to='core.financialledger')),
                ('created_by', models.ForeignKey(on_delete=models.PROTECT, related_name='financial_reversals', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        )
    ]
