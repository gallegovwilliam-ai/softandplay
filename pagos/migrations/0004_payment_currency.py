from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('pagos','0003_payment_records')]
    operations = [migrations.AddField(model_name='paymentrecord', name='currency', field=models.CharField(default='COP', max_length=3)), migrations.AddField(model_name='paymentrecord75', name='currency', field=models.CharField(default='COP', max_length=3))]
