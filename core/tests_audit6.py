from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase

from core.financial_rules import (
    money, calculate_prize_pool, split_prize_pool, apply_tax, reconcile,
)
from core.models import FinancialLedger


class FinancialRulesAudit6Tests(TestCase):
    def test_money_rounding(self):
        self.assertEqual(money('10.005'), Decimal('10.01'))
        self.assertEqual(money('10.004'), Decimal('10.00'))

    def test_prize_distribution_and_tax(self):
        pool = calculate_prize_pool('10000', 100)
        gross, components = split_prize_pool(pool, [('50', 1), ('30', 2), ('20', 4)])
        self.assertEqual(pool, Decimal('1000000.00'))
        self.assertEqual(components, [Decimal('500000.00'), Decimal('150000.00'), Decimal('50000.00')])
        self.assertEqual(gross, Decimal('700000.00'))
        tax, net = apply_tax(gross, '10')
        self.assertEqual(tax, Decimal('70000.00'))
        self.assertEqual(net, Decimal('630000.00'))
        self.assertTrue(reconcile(pool, gross, tax, net))

    def test_invalid_configuration_is_rejected(self):
        pool = calculate_prize_pool('10000', 10)
        with self.assertRaises(ValueError):
            split_prize_pool(pool, [('101', 1)])
        with self.assertRaises(ValueError):
            split_prize_pool(pool, [('60', 1), ('50', 1)])
        with self.assertRaises(ValueError):
            split_prize_pool(pool, [('50', 0)])

    def test_ledger_unique_key_is_idempotent(self):
        user = User.objects.create_user(username='audit6_admin', password='test-password')
        defaults = dict(
            user=user, entry_type=FinancialLedger.ENTRY_CREDIT,
            amount=Decimal('100.00'), currency='COP',
            reference_type='Impresion', reference_id='123',
            description='Premio',
        )
        a, created_a = FinancialLedger.objects.get_or_create(unique_key='AUDIT6:123', defaults=defaults)
        b, created_b = FinancialLedger.objects.get_or_create(unique_key='AUDIT6:123', defaults=defaults)
        self.assertTrue(created_a)
        self.assertFalse(created_b)
        self.assertEqual(a.pk, b.pk)
        self.assertEqual(FinancialLedger.objects.filter(unique_key='AUDIT6:123').count(), 1)
