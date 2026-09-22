from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_userprofile_validado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='validado',
            field=models.BooleanField(default=False),
        ),
    ]
