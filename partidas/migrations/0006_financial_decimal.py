from django.db import migrations, models
from decimal import Decimal, InvalidOperation

def d(v):
    try: return Decimal(str(v or '0')).quantize(Decimal('0.01'))
    except (InvalidOperation, TypeError, ValueError): return Decimal('0.00')

def copy_values(apps, schema_editor):
    for name in ('Partida','Partida75'):
        M=apps.get_model('partidas',name)
        for obj in M.objects.all().iterator():
            updates={}
            for i in range(1,11): updates['monto_{}_decimal'.format(i)] = d(getattr(obj,'monto_{}'.format(i)))
            updates['monto_carton_decimal']=d(obj.monto_carton)
            updates['monto_acumulado_decimal']=d(obj.monto_acumulado)
            updates['impuesto_decimal']=d(obj.impuesto)
            updates['total_decimal']=d(obj.total)
            for k,v in updates.items(): setattr(obj,k,v)
            obj.save(update_fields=list(updates))

class Migration(migrations.Migration):
    dependencies=[('partidas','0005_hardening_constraints')]
    operations=[]
    for name in ('partida','partida75'):
        operations += [migrations.AddField(name,'monto_{}_decimal'.format(i),models.DecimalField(decimal_places=2,default=0,max_digits=14)) for i in range(1,11)]
        operations += [migrations.AddField(name,'monto_carton_decimal',models.DecimalField(decimal_places=2,default=0,max_digits=14)), migrations.AddField(name,'monto_acumulado_decimal',models.DecimalField(decimal_places=2,default=0,max_digits=14)), migrations.AddField(name,'impuesto_decimal',models.DecimalField(decimal_places=2,default=0,max_digits=14)), migrations.AddField(name,'total_decimal',models.DecimalField(decimal_places=2,default=0,max_digits=14))]
    operations.append(migrations.RunPython(copy_values,migrations.RunPython.noop))
