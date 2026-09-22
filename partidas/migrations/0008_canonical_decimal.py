from django.db import migrations, models
from decimal import Decimal, InvalidOperation

MONEY = ['monto_1','monto_2','monto_3','monto_4','monto_5','monto_6','monto_7','monto_8','monto_9','monto_10','monto_carton','monto_acumulado','impuesto','total']
PCTS = ['porciento_1','porciento_2','porciento_3','porciento_4','porciento_5','porciento_6','porciento_7','porciento_8','porciento_9','porciento_10']

def copy_shadow_to_canonical(apps, schema_editor):
    for model_name in ('Partida','Partida75'):
        Model = apps.get_model('partidas', model_name)
        for obj in Model.objects.all().iterator():
            updates={}
            for name in MONEY:
                shadow = getattr(obj, name + '_decimal', None)
                value = shadow if shadow not in (None,'') else getattr(obj,name,None)
                try: updates[name]=Decimal(str(value or '0')).quantize(Decimal('0.01'))
                except (InvalidOperation,TypeError,ValueError): updates[name]=Decimal('0.00')
            for name in PCTS:
                try: updates[name]=Decimal(str(getattr(obj,name) or '0')).quantize(Decimal('0.01'))
                except (InvalidOperation,TypeError,ValueError): updates[name]=Decimal('0.00')
            Model.objects.filter(pk=obj.pk).update(**updates)

class Migration(migrations.Migration):
    dependencies=[('partidas','0007_partidasequence')]
    operations=[
        migrations.RunPython(copy_shadow_to_canonical, migrations.RunPython.noop),
    ] + [
        migrations.AlterField('partida', n, models.DecimalField(max_digits=14, decimal_places=2, default=0, blank=True)) for n in MONEY
    ] + [
        migrations.AlterField('partida75', n, models.DecimalField(max_digits=14, decimal_places=2, default=0, blank=True)) for n in MONEY
    ] + [
        migrations.AlterField('partida', n, models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)) for n in PCTS
    ] + [
        migrations.AlterField('partida75', n, models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)) for n in PCTS
    ] + [
        migrations.RemoveField('partida', n + '_decimal') for n in MONEY
    ] + [
        migrations.RemoveField('partida75', n + '_decimal') for n in MONEY
    ]
