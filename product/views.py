from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, ProductComment

def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        parent_id, body = request.POST.get('parent_id'), request.POST.get('body')
        ProductComment.objects.create(product=product, parent_id=parent_id, body=body, user=request.user)
    return render(request, 'product/product-detail.html', context={'object':product})