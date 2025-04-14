from django import template
from product.models import ProductComment, Product

register = template.Library()

@register.simple_tag
def cmt_counter(id):
    return len(ProductComment.objects.filter(product=Product.objects.get(pk=id)))