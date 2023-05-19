from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'active', 'discount']
    list_filter = ['active', 'valid_to', 'valid_from']
    search_fields = ['code']
