from django.contrib import admin
from .models import Settlement, Settlement75, PaymentRecord, PaymentRecord75

class ReadOnlySettlementAdmin(admin.ModelAdmin):
    list_display = ('partida','sold_cards','pool','prize_gross','tax','prize_net','settled_at')
    readonly_fields = tuple(f.name for f in Settlement._meta.fields)
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

class ReadOnlySettlement75Admin(admin.ModelAdmin):
    list_display = ('partida','sold_cards','pool','prize_gross','tax','prize_net','settled_at')
    readonly_fields = tuple(f.name for f in Settlement75._meta.fields)
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

class ReadOnlyPaymentAdmin(admin.ModelAdmin):
    readonly_fields = tuple(f.name for f in PaymentRecord._meta.fields)
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

class ReadOnlyPayment75Admin(admin.ModelAdmin):
    readonly_fields = tuple(f.name for f in PaymentRecord75._meta.fields)
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

admin.site.register(Settlement, ReadOnlySettlementAdmin)
admin.site.register(Settlement75, ReadOnlySettlement75Admin)
admin.site.register(PaymentRecord, ReadOnlyPaymentAdmin)
admin.site.register(PaymentRecord75, ReadOnlyPayment75Admin)

from .models import SaleRecord, SaleRecord75, CashReconciliation

class ReadOnlySaleAdmin(admin.ModelAdmin):
    readonly_fields = tuple(f.name for f in SaleRecord._meta.fields)
    list_display = ('id','header','quantity','unit_price','amount','status','approved_at')
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

class ReadOnlySale75Admin(admin.ModelAdmin):
    readonly_fields = tuple(f.name for f in SaleRecord75._meta.fields)
    list_display = ('id','header','quantity','unit_price','amount','status','approved_at')
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

class ReadOnlyCashReconciliationAdmin(admin.ModelAdmin):
    readonly_fields = tuple(f.name for f in CashReconciliation._meta.fields)
    list_display = ('date','sales','payouts','refunds','net_cash','generated_at','generated_by')
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

admin.site.register(SaleRecord, ReadOnlySaleAdmin)
admin.site.register(SaleRecord75, ReadOnlySale75Admin)
admin.site.register(CashReconciliation, ReadOnlyCashReconciliationAdmin)

from .models import FinancialReversal

@admin.register(FinancialReversal)
class ReadOnlyFinancialReversalAdmin(admin.ModelAdmin):
    list_display = ('original_entry', 'reversal_entry', 'created_by', 'reason', 'created_at')
    readonly_fields = tuple(f.name for f in FinancialReversal._meta.fields)
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
