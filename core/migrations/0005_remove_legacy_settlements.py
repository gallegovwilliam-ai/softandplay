from django.db import migrations


def protect_legacy_settlements(apps, schema_editor):
    """Do not silently destroy data from the obsolete core settlement tables."""
    connection = schema_editor.connection
    tables = set(connection.introspection.table_names())
    for table in ('core_settlement', 'core_settlement75'):
        if table in tables:
            with connection.cursor() as cursor:
                cursor.execute('SELECT COUNT(*) FROM "{}"'.format(table))
                count = cursor.fetchone()[0]
            if count:
                raise RuntimeError(
                    'La tabla legacy {} contiene {} registros. '
                    'Migra/revisa esos datos antes de continuar.'.format(table, count)
                )


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_settlements'),
    ]

    operations = [
        migrations.RunPython(protect_legacy_settlements, migrations.RunPython.noop),
        migrations.DeleteModel(name='Settlement'),
        migrations.DeleteModel(name='Settlement75'),
    ]
