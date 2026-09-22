from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.utils import timezone
from .models import Wallet, TransactionWallet
from core.financial_ledger import ledger_entry
from core.models import FinancialLedger

CENT = Decimal('0.01')

def move_wallet(*, user, amount, transaction_type, description='', request=None, unique_key=''):
    amount = Decimal(str(amount)).quantize(CENT, rounding=ROUND_HALF_UP)
    if amount == 0:
        raise ValueError('El movimiento no puede ser cero')
    if not unique_key or not str(unique_key).strip():
        raise ValueError('El movimiento de wallet requiere una clave única')
    with transaction.atomic():
        existing = FinancialLedger.objects.filter(unique_key=unique_key).first()
        if existing:
            try:
                tx = TransactionWallet.objects.get(pk=existing.reference_id)
                wallet = Wallet.objects.get(user=user)
                return tx, wallet
            except TransactionWallet.DoesNotExist:
                raise ValueError('Existe un asiento de wallet sin transacción asociada')
        wallet = Wallet.objects.select_for_update().get(user=user)
        new_balance = wallet.balance + amount
        if new_balance < 0:
            raise ValueError('Saldo insuficiente')
        wallet.balance = new_balance
        wallet.save(update_fields=['balance'])
        tx = TransactionWallet.objects.create(wallet=wallet, transaction_type=transaction_type, description=description[:200], amount=abs(amount), date=timezone.now())
        ledger_entry(user=user, entry_type='CREDITO' if amount > 0 else 'DEBITO', amount=abs(amount), reference_type='TransactionWallet', reference_id=tx.pk, description=description, request=request, unique_key=unique_key)
        return tx, wallet
