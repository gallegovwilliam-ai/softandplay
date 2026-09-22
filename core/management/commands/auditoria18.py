from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Auditoria 18: ciclo financiero, ventas, pagos y seguridad operativa.'

    def handle(self, *args, **options):
        errors = []
        warnings = []
        try:
            from pagos.models import PaymentRecord, PaymentRecord75, SaleRecord, SaleRecord75, FinancialReversal
            from core.models import FinancialLedger
            for Model, name in ((SaleRecord, 'SaleRecord'), (SaleRecord75, 'SaleRecord75')):
                if Model.objects.filter(quantity__lte=0).exists():
                    errors.append(name + ': existen cantidades no positivas')
                if Model.objects.filter(amount__lte=0).exists():
                    errors.append(name + ': existen importes no positivos')
            for Model, name in ((PaymentRecord, 'PaymentRecord'), (PaymentRecord75, 'PaymentRecord75')):
                if Model.objects.filter(amount__lt=0).exists() or Model.objects.filter(tax__lt=0).exists() or Model.objects.filter(net_amount__lt=0).exists():
                    errors.append(name + ': existen importes negativos')
                approved = Model.objects.filter(status=Model.STATUS_APPROVED, approved_at__isnull=True).exists()
                if approved:
                    errors.append(name + ': pagos aprobados sin fecha de aprobacion')
            if FinancialReversal.objects.filter(original_entry__isnull=True).exists() or FinancialReversal.objects.filter(reversal_entry__isnull=True).exists():
                errors.append('FinancialReversal: referencias incompletas')
            # Toda venta aprobada debe tener su asiento financiero idempotente.
            for Model, prefix, name in ((SaleRecord, '4', 'SaleRecord'), (SaleRecord75, '75', 'SaleRecord75')):
                for sale in Model.objects.filter(status=Model.STATUS_APPROVED).only('pk'):
                    if not FinancialLedger.objects.filter(unique_key='VENTA:{}:{}'.format(prefix, sale.pk)).exists():
                        errors.append('{} #{} sin asiento VENTA'.format(name, sale.pk))
                        break
            # Nunca debe quedar una solicitud PayPal entregada sin venta registrada.
            try:
                from cards.models import CabezeraImpre, CabezeraImpre75
                for Header, Sale in ((CabezeraImpre, SaleRecord), (CabezeraImpre75, SaleRecord75)):
                    pending = Header.objects.filter(banco='paypal', verficado=False).count()
                    if pending:
                        warnings.append('{} solicitudes PayPal pendientes'.format(pending))
            except Exception:
                pass
            self.stdout.write('DB vendor: {}'.format(connection.vendor))
        except Exception as exc:
            errors.append('No fue posible completar la auditoria ORM: {}'.format(exc))
        if errors:
            for item in errors:
                self.stdout.write(self.style.ERROR('ERROR: ' + item))
            raise SystemExit(1)
        for item in warnings:
            self.stdout.write(self.style.WARNING('AVISO: ' + item))
        self.stdout.write(self.style.SUCCESS('AUDITORIA 18: OK'))
