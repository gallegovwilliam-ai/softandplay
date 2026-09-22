from django.db import migrations, models
class Migration(migrations.Migration):
 dependencies=[('configuracion','0007_impuesto_decimal')]
 operations=[migrations.AddConstraint('config', models.CheckConstraint(check=models.Q(impuesto__gte=0) & models.Q(impuesto__lte=100), name='config_impuesto_range'))]
