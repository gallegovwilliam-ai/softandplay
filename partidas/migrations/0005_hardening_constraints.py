from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('partidas', '0004_auto_20210114_1505'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='partida',
            constraint=models.UniqueConstraint(fields=('fecha', 'partida'), name='uniq_partida_fecha_num'),
        ),
        migrations.AddConstraint(
            model_name='partida75',
            constraint=models.UniqueConstraint(fields=('fecha', 'partida'), name='uniq_partida75_fecha_num'),
        ),
        migrations.AddConstraint(
            model_name='jugada',
            constraint=models.UniqueConstraint(fields=('partida', 'balota'), name='uniq_jugada_partida_balota'),
        ),
        migrations.AddConstraint(
            model_name='jugada75',
            constraint=models.UniqueConstraint(fields=('partida', 'balota'), name='uniq_jugada75_partida_balota'),
        ),
    ]
