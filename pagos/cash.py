from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum
from core.models import FinancialLedger
from .models import CashReconciliation


def reconcile_day(day, user, notes=''):
    """Construye una conciliación diaria de caja a partir del ledger inmutable."""
    with transaction.atomic():
        credits = FinancialLedger.objects.filter(created_at__date=day, entry_type=FinancialLedger.ENTRY_CREDIT, reference_type__in=['SaleRecord','SaleRecord75']).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        # Solo PaymentRecord representa salida real de caja. Los asientos de premio
        # históricos (Impresion/Impresion75) no se cuentan porque no son pagos de caja.
        payouts = FinancialLedger.objects.filter(created_at__date=day, entry_type=FinancialLedger.ENTRY_DEBIT, reference_type__in=['PaymentRecord','PaymentRecord75']).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        refunds = FinancialLedger.objects.filter(created_at__date=day, entry_type=FinancialLedger.ENTRY_DEBIT, reference_type__in=['Refund','Refund75']).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        net = credits - payouts - refunds
        obj, _ = CashReconciliation.objects.update_or_create(
            date=day,
            defaults={'sales': credits, 'payouts': payouts, 'refunds': refunds, 'net_cash': net, 'generated_by': user, 'notes': notes[:2000]},
        )
        return obj
