from product.models import Product, Category, Brand


def contextprocessorsfunction(request):
    return {
        'trend_women_objects': Product.objects.filter(is_trend=True),
        'category_list': Category.objects.all(),
        'brand_list': Brand.objects.all()
    }