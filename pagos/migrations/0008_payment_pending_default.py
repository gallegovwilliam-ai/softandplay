from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('pagos', '0007_financial_reversals')]
    operations = [
        migrations.AlterField(
            model_name='paymentrecord', name='status',
            field=models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('APROBADO', 'Aprobado'), ('RECHAZADO', 'Rechazado'), ('ANULADO', 'Anulado')], default='PENDIENTE', max_length=12),
        ),
        migrations.AlterField(
            model_name='paymentrecord75', name='status',
            field=models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('APROBADO', 'Aprobado'), ('RECHAZADO', 'Rechazado'), ('ANULADO', 'Anulado')], default='PENDIENTE', max_length=12),
        ),
    ]
