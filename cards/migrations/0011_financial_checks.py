from django.db import migrations, models
class Migration(migrations.Migration):
 dependencies=[('cards','0010_canonical_decimal')]
 operations=[
  migrations.AddConstraint('impresion', models.CheckConstraint(check=models.Q(monto__gte=0), name='impresion_monto_nonnegative')),
  migrations.AddConstraint('impresion', models.CheckConstraint(check=models.Q(impuesto__gte=0), name='impresion_impuesto_nonnegative')),
  migrations.AddConstraint('impresion', models.CheckConstraint(check=models.Q(total__gte=0), name='impresion_total_nonnegative')),
  migrations.AddConstraint('impresion75', models.CheckConstraint(check=models.Q(monto__gte=0), name='impresion75_monto_nonnegative')),
  migrations.AddConstraint('impresion75', models.CheckConstraint(check=models.Q(impuesto__gte=0), name='impresion75_impuesto_nonnegative')),
  migrations.AddConstraint('impresion75', models.CheckConstraint(check=models.Q(total__gte=0), name='impresion75_total_nonnegative')),
 ]
