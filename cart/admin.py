from django.contrib import admin
from cart.models import CouponCode

@admin.register(CouponCode)
class Admin(admin.ModelAdmin):
    pass