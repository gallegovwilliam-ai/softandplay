from django.db import migrations, models
from decimal import Decimal, InvalidOperation

def to_decimal(v):
    try:
        return Decimal(str(v or '0')).quantize(Decimal('0.01'))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal('0.00')

def copy_values(apps, schema_editor):
    for name in ('Impresion','Impresion75'):
        M=apps.get_model('cards', name)
        for obj in M.objects.all().iterator():
            obj.monto_decimal=to_decimal(obj.monto)
            obj.impuesto_decimal=to_decimal(obj.impuesto)
            obj.total_decimal=to_decimal(obj.total)
            obj.save(update_fields=['monto_decimal','impuesto_decimal','total_decimal'])

class Migration(migrations.Migration):
    dependencies=[('cards','0008_auto_20210114_1323')]
    operations=[
        migrations.AddField('impresion','monto_decimal',models.DecimalField(decimal_places=2,default=0,max_digits=14)),
        migrations.AddField('impresion','impuesto_decimal',models.DecimalField(decimal_places=2,default=0,max_digits=14)),
        migrations.AddField('impresion','total_decimal',models.DecimalField(decimal_places=2,default=0,max_digits=14)),
        migrations.AddField('impresion75','monto_decimal',models.DecimalField(decimal_places=2,default=0,max_digits=14)),
        migrations.AddField('impresion75','impuesto_decimal',models.DecimalField(decimal_places=2,default=0,max_digits=14)),
        migrations.AddField('impresion75','total_decimal',models.DecimalField(decimal_places=2,default=0,max_digits=14)),
        migrations.RunPython(copy_values,migrations.RunPython.noop),
    ]
