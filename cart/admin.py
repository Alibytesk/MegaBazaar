from django.contrib import admin
from cart.models import CouponCode, Order, OrderObject

class OrderObjectAdmin(admin.TabularInline):
    model = OrderObject
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('is_paid', 'user')
    inlines = (OrderObjectAdmin,)
    list_filter = ('is_paid',)
@admin.register(CouponCode)
class Admin(admin.ModelAdmin):
    pass