from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal
import datetime

class Wallet(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('10.00'))

    class Meta:
        constraints = [models.CheckConstraint(check=models.Q(balance__gte=0), name='wallet_balance_nonnegative')]

@receiver(post_save,sender=User)
def create_wallet(sender,instance,created,**kwargs):
	if created:
		Wallet.objects.create(user=instance)

class TransactionWallet(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateTimeField(editable=False)
    class Meta:
        constraints = [models.CheckConstraint(check=models.Q(amount__gte=0), name='transactionwallet_amount_nonnegative')]

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.now()
        return super(TransactionWallet, self).save(*args, **kwargs)    


