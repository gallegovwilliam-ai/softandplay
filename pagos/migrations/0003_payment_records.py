from django.db import migrations, models
from django.conf import settings
from decimal import Decimal

class Migration(migrations.Migration):
    dependencies = [
        ('pagos', '0002_mensajecarton75'),
        ('cards', '0008_auto_20210114_1323'),
    ]
    operations = [
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('APROBADO', 'Aprobado'), ('RECHAZADO', 'Rechazado'), ('ANULADO', 'Anulado')], default='APROBADO', max_length=12)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
                ('tax', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
                ('net_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
                ('method', models.CharField(blank=True, max_length=50)),
                ('transaction_reference', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('carton', models.OneToOneField(on_delete=models.deletion.PROTECT, related_name='payment_record', to='cards.Impresion')),
                ('processed_by', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='processed_payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord75',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('APROBADO', 'Aprobado'), ('RECHAZADO', 'Rechazado'), ('ANULADO', 'Anulado')], default='APROBADO', max_length=12)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
                ('tax', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
                ('net_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
                ('method', models.CharField(blank=True, max_length=50)),
                ('transaction_reference', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('carton', models.OneToOneField(on_delete=models.deletion.PROTECT, related_name='payment_record', to='cards.Impresion75')),
                ('processed_by', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='processed_payments75', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
