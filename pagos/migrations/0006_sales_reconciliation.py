from django.db import migrations, models
from django.conf import settings
from decimal import Decimal
import django.db.models.deletion


def backfill_sales(apps, schema_editor):
    Cabezera = apps.get_model('cards', 'CabezeraImpre')
    Cabezera75 = apps.get_model('cards', 'CabezeraImpre75')
    Sale = apps.get_model('pagos', 'SaleRecord')
    Sale75 = apps.get_model('pagos', 'SaleRecord75')
    Partida = apps.get_model('partidas', 'Partida')
    Partida75 = apps.get_model('partidas', 'Partida75')
    User = apps.get_model('auth', 'User')
    Ledger = apps.get_model('core', 'FinancialLedger')
    for h in Cabezera.objects.filter(verficado=True):
        try: q=int(h.cantidad or 0)
        except (TypeError, ValueError): q=0
        if q>0 and not Sale.objects.filter(header_id=h.pk).exists():
            p=Partida.objects.get(pk=h.partida_id)
            price=Decimal(str(p.monto_carton_decimal or p.monto_carton or '0')).quantize(Decimal('0.01'))
            sale=Sale.objects.create(header_id=h.pk, processed_by_id=h.user_id, quantity=q, unit_price=price, amount=(price*q).quantize(Decimal('0.01')), approved_at=h.fecha)
            Ledger.objects.get_or_create(unique_key='VENTA:4:{}'.format(sale.pk), defaults={'user_id':h.user_id,'entry_type':'CREDITO','amount':sale.amount,'currency':'COP','reference_type':'SaleRecord','reference_id':str(sale.pk),'description':'Venta histórica aprobada'})
    for h in Cabezera75.objects.filter(verficado=True):
        try: q=int(h.cantidad or 0)
        except (TypeError, ValueError): q=0
        if q>0 and not Sale75.objects.filter(header_id=h.pk).exists():
            p=Partida75.objects.get(pk=h.partida_id)
            price=Decimal(str(p.monto_carton_decimal or p.monto_carton or '0')).quantize(Decimal('0.01'))
            sale=Sale75.objects.create(header_id=h.pk, processed_by_id=h.user_id, quantity=q, unit_price=price, amount=(price*q).quantize(Decimal('0.01')), approved_at=h.fecha)
            Ledger.objects.get_or_create(unique_key='VENTA:75:{}'.format(sale.pk), defaults={'user_id':h.user_id,'entry_type':'CREDITO','amount':sale.amount,'currency':'COP','reference_type':'SaleRecord75','reference_id':str(sale.pk),'description':'Venta histórica aprobada'})

class Migration(migrations.Migration):
    dependencies=[('pagos','0005_settlements'),('cards','0009_financial_decimal'),('core','0003_financialledger'),('partidas','0006_financial_decimal'),migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='SaleRecord',fields=[('id',models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('status',models.CharField(choices=[('APROBADA','Aprobada'),('ANULADA','Anulada')],default='APROBADA',max_length=10)),('quantity',models.PositiveIntegerField(default=0)),('unit_price',models.DecimalField(decimal_places=2,default=Decimal('0.00'),max_digits=14)),('amount',models.DecimalField(decimal_places=2,default=Decimal('0.00'),max_digits=14)),('currency',models.CharField(default='COP',max_length=3)),('approved_at',models.DateTimeField(blank=True,null=True)),('created_at',models.DateTimeField(auto_now_add=True)),('header',models.OneToOneField(on_delete=django.db.models.deletion.PROTECT,related_name='sale_record',to='cards.cabezeraimpre')),('processed_by',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='sales_recorded',to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='SaleRecord75',fields=[('id',models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('status',models.CharField(choices=[('APROBADA','Aprobada'),('ANULADA','Anulada')],default='APROBADA',max_length=10)),('quantity',models.PositiveIntegerField(default=0)),('unit_price',models.DecimalField(decimal_places=2,default=Decimal('0.00'),max_digits=14)),('amount',models.DecimalField(decimal_places=2,default=Decimal('0.00'),max_digits=14)),('currency',models.CharField(default='COP',max_length=3)),('approved_at',models.DateTimeField(blank=True,null=True)),('created_at',models.DateTimeField(auto_now_add=True)),('header',models.OneToOneField(on_delete=django.db.models.deletion.PROTECT,related_name='sale_record75',to='cards.cabezeraimpre75')),('processed_by',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='sales_recorded75',to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='CashReconciliation',fields=[('id',models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('date',models.DateField(unique=True)),('sales',models.DecimalField(decimal_places=2,default=Decimal('0.00'),max_digits=14)),('payouts',models.DecimalField(decimal_places=2,default=Decimal('0.00'),max_digits=14)),('refunds',models.DecimalField(decimal_places=2,default=Decimal('0.00'),max_digits=14)),('net_cash',models.DecimalField(decimal_places=2,default=Decimal('0.00'),max_digits=14)),('generated_at',models.DateTimeField(auto_now_add=True)),('generated_by',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='cash_reconciliations',to=settings.AUTH_USER_MODEL)),('notes',models.TextField(blank=True))]),
        migrations.RunPython(backfill_sales, migrations.RunPython.noop),
    ]
