from django import template
from product.models import ProductComment, Product, Brand

register = template.Library()

@register.simple_tag
def cmt_counter(id):
    return len(ProductComment.objects.filter(product=Product.objects.get(pk=id)))
@register.simple_tag
def brand_counter(id):
    return len(Product.objects.filter(brand_id=Brand.objects.get(pk=id)))