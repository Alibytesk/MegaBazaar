from django.contrib import admin
from product.models import Product, Information, ProductComment, ProductImage, Category, Size, Color


class InformationAdmin(admin.StackedInline):
    model = Information
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount')
    inlines = (InformationAdmin,)

@admin.register(ProductComment, ProductImage, Category, Color, Size)
class Admin(admin.ModelAdmin):
    pass
