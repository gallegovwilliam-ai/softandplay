from django.db import migrations, models
from decimal import Decimal, InvalidOperation


def copy_shadow_to_canonical(apps, schema_editor):
    for model_name in ('Impresion', 'Impresion75'):
        Model = apps.get_model('cards', model_name)
        for obj in Model.objects.all().iterator():
            def d(name, fallback):
                value = getattr(obj, name, None)
                if value in (None, ''):
                    value = fallback
                try:
                    return Decimal(str(value or '0')).quantize(Decimal('0.01'))
                except (InvalidOperation, TypeError, ValueError):
                    return Decimal('0.00')
            obj.monto = d('monto_decimal', obj.monto)
            obj.impuesto = d('impuesto_decimal', obj.impuesto)
            obj.total = d('total_decimal', obj.total)
            obj.save(update_fields=['monto', 'impuesto', 'total'])


class Migration(migrations.Migration):
    dependencies = [('cards', '0009_financial_decimal')]
    operations = [
        migrations.RunPython(copy_shadow_to_canonical, migrations.RunPython.noop),
        migrations.AlterField('impresion', 'monto', models.DecimalField(max_digits=14, decimal_places=2, default=0, blank=True)),
        migrations.AlterField('impresion', 'impuesto', models.DecimalField(max_digits=14, decimal_places=2, default=0, blank=True)),
        migrations.AlterField('impresion', 'total', models.DecimalField(max_digits=14, decimal_places=2, default=0, blank=True)),
        migrations.AlterField('impresion75', 'monto', models.DecimalField(max_digits=14, decimal_places=2, default=0, blank=True)),
        migrations.AlterField('impresion75', 'impuesto', models.DecimalField(max_digits=14, decimal_places=2, default=0, blank=True)),
        migrations.AlterField('impresion75', 'total', models.DecimalField(max_digits=14, decimal_places=2, default=0, blank=True)),
        migrations.RemoveField('impresion', 'monto_decimal'),
        migrations.RemoveField('impresion', 'impuesto_decimal'),
        migrations.RemoveField('impresion', 'total_decimal'),
        migrations.RemoveField('impresion75', 'monto_decimal'),
        migrations.RemoveField('impresion75', 'impuesto_decimal'),
        migrations.RemoveField('impresion75', 'total_decimal'),
    ]
