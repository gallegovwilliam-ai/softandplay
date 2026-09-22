from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [('core', '0002_auditlog')]
    operations = [migrations.CreateModel(
        name='FinancialLedger',
        fields=[
            ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('entry_type', models.CharField(choices=[('CREDITO','Crédito'),('DEBITO','Débito')], max_length=10)),
            ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
            ('currency', models.CharField(default='COP', max_length=3)),
            ('reference_type', models.CharField(max_length=80)),
            ('reference_id', models.CharField(max_length=80)),
            ('unique_key', models.CharField(max_length=160, unique=True)),
            ('description', models.CharField(blank=True, max_length=255)),
            ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('user', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name='financial_entries', to=settings.AUTH_USER_MODEL)),
        ],
        options={'ordering':['-created_at']},
    ), migrations.AddIndex(model_name='financialledger', index=models.Index(fields=['reference_type','reference_id'], name='core_financ_refere_8e7d9c_idx')), migrations.AddIndex(model_name='financialledger', index=models.Index(fields=['user','created_at'], name='core_financ_user_id_2b7b4a_idx'))]
