from django.db import migrations, models


def convert_quantity(apps, schema_editor):
    for model_name in ('CabezeraImpre', 'CabezeraImpre75'):
        Model = apps.get_model('cards', model_name)
        for obj in Model.objects.all().iterator():
            raw = obj.cantidad
            try:
                value = int(raw or 0)
            except (TypeError, ValueError):
                value = 0
            if value < 0:
                value = 0
            Model.objects.filter(pk=obj.pk).update(cantidad=value)


class Migration(migrations.Migration):
    dependencies = [('cards', '0011_financial_checks')]
    operations = [
        migrations.RunPython(convert_quantity, migrations.RunPython.noop),
        migrations.AlterField('cabezeraimpre', 'cantidad', models.PositiveIntegerField(default=0)),
        migrations.AlterField('cabezeraimpre75', 'cantidad', models.PositiveIntegerField(default=0)),
    ]
