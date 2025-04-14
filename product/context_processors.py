from product.models import Product, Category


def contextprocessorsfunction(request):
    return {
        'category_list': Category.objects.all(),
        'trend_women_objects': Product.objects.filter(is_trend=True)
    }