from django.db import migrations, models

MONEY=['monto_1','monto_2','monto_3','monto_4','monto_5','monto_6','monto_7','monto_8','monto_9','monto_10','monto_carton','monto_acumulado','impuesto','total']
PCTS=['porciento_1','porciento_2','porciento_3','porciento_4','porciento_5','porciento_6','porciento_7','porciento_8','porciento_9','porciento_10']
class Migration(migrations.Migration):
 dependencies=[('partidas','0008_canonical_decimal')]
 operations=[]
 for n in MONEY:
  operations.append(migrations.AddConstraint('partida', models.CheckConstraint(check=models.Q(**{n+'__gte':0}), name='partida_'+n+'_nonnegative')))
  operations.append(migrations.AddConstraint('partida75', models.CheckConstraint(check=models.Q(**{n+'__gte':0}), name='partida75_'+n+'_nonnegative')))
 for n in PCTS:
  operations.append(migrations.AddConstraint('partida', models.CheckConstraint(check=models.Q(**{n+'__gte':0}) & models.Q(**{n+'__lte':100}), name='partida_'+n+'_range')))
  operations.append(migrations.AddConstraint('partida75', models.CheckConstraint(check=models.Q(**{n+'__gte':0}) & models.Q(**{n+'__lte':100}), name='partida75_'+n+'_range')))
