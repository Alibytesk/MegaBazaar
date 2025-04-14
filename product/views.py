from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, ProductComment
from django.core.paginator import Paginator

def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        parent_id, body = request.POST.get('parent_id'), request.POST.get('body')
        ProductComment.objects.create(product=product, parent_id=parent_id, body=body, user=request.user)
    return render(request, 'product/product-detail.html', context={'object':product})
def products_list(request):
    if request.GET.get('category'):
        products = Product.objects.filter(category__title__icontains=request.GET.get('category'))
        if products:
            paginator = Paginator(products, 3)
            products = paginator.get_page(request.GET.get('page'))
            return render(request, 'product/product-list.html', context={'objects':products})
    elif request.GET.get('brand'):
        products = Product.objects.filter(brand__title__icontains=request.GET.get('brand'))
        if products:
            paginator = Paginator(products, 3)
            products = paginator.get_page(request.GET.get('page'))
            return render(request, 'product/product-list.html', context={'objects':products})
    return redirect('home:home')