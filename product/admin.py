from django.contrib import admin
from product.models import Product, Information, ProductComment, ProductImage, Category, Size, Color, Brand, PriceRange, Like


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
class InformationAdmin(admin.StackedInline):
    model = Information
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount', 'is_trend')
    inlines = (ProductImageAdmin, InformationAdmin,)

@admin.register(ProductComment, ProductImage, Like, Category, Color, Size, Brand, PriceRange)
class Admin(admin.ModelAdmin):
    pass
