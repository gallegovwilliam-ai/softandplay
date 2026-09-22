from django.db import migrations, models
class Migration(migrations.Migration):
 dependencies=[('partidas','0009_financial_checks')]
 operations=[
  migrations.AlterField('partida','cartones_vendidos',models.PositiveIntegerField(default=0)),
  migrations.AlterField('partida75','cartones_vendidos',models.PositiveIntegerField(default=0)),
 ]
