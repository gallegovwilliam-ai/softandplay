from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_financialledger'),
        ('partidas', '0006_financial_decimal'),
    ]
    operations = [
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('LIQUIDADA', 'Liquidada')], default='LIQUIDADA', max_length=12)),
                ('sold_cards', models.PositiveIntegerField(default=0)),
                ('pool', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('gross_prize', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('net_prize', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('settled_at', models.DateTimeField(auto_now_add=True)),
                ('partida', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='settlement', to='partidas.partida')),
                ('settled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='settlements', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Settlement75',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('LIQUIDADA', 'Liquidada')], default='LIQUIDADA', max_length=12)),
                ('sold_cards', models.PositiveIntegerField(default=0)),
                ('pool', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('gross_prize', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('net_prize', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('settled_at', models.DateTimeField(auto_now_add=True)),
                ('partida', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='settlement', to='partidas.partida75')),
                ('settled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='settlements75', to='auth.user')),
            ],
        ),
    ]
