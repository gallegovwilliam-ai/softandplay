from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies=[('partidas','0006_financial_decimal')]
    operations=[migrations.CreateModel(name='PartidaSequence', fields=[('id',models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('fecha',models.DateField()),('tipo',models.CharField(choices=[('LOTO','Lotería Mexicana'),('BINGO75','Bingo 75')],max_length=10)),('ultimo_numero',models.PositiveIntegerField(default=0))]),migrations.AddConstraint(model_name='partidasequence',constraint=models.UniqueConstraint(fields=['fecha','tipo'],name='uniq_partida_sequence_fecha_tipo'))]
