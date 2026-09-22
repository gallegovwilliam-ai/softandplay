from django.db import migrations, models
from decimal import Decimal, InvalidOperation

def to_decimal(apps, schema_editor):
    Config=apps.get_model('configuracion','Config')
    for obj in Config.objects.all():
        try: v=Decimal(str(obj.impuesto or '0')).quantize(Decimal('0.01'))
        except (InvalidOperation,TypeError,ValueError): v=Decimal('0.00')
        Config.objects.filter(pk=obj.pk).update(impuesto=v)

class Migration(migrations.Migration):
    dependencies=[('configuracion','0006_config_impuesto')]
    operations=[migrations.RunPython(to_decimal,migrations.RunPython.noop), migrations.AlterField('config','impuesto',models.DecimalField(max_digits=5,decimal_places=2,default=12))]
