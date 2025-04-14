from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, ProductComment, PriceRange
from django.core.paginator import Paginator

def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        parent_id, body = request.POST.get('parent_id'), request.POST.get('body')
        ProductComment.objects.create(product=product, parent_id=parent_id, body=body, user=request.user)
    return render(request, 'product/product-detail.html', context={'object':product})
def products_list(request):
    if request.GET.get('category'):
        if request.GET.get('apricerange') and request.GET.get('bpricerange'):
            products = Product.objects.filter(
                category__title__icontains=request.GET.get('category'),
                price_range__a_price__lte=request.GET.get('apricerange'),
                price_range__b_price__gte=request.GET.get('bpricerange'),
            )
        else:
            products = Product.objects.filter(category__title__icontains=request.GET.get('category'))

    elif request.GET.get('brand'):
        if request.GET.get('apricerange') and request.GET.get('bpricerange'):
            products = Product.objects.filter(
                brand__title__icontains=request.GET.get('brand'),
                price_range__a_price__lte=request.GET.get('apricerange'),
                price_range__b_price__gte=request.GET.get('bpricerange'),
            )
        else:
            products = Product.objects.filter(brand__title__icontains=request.GET.get('brand'))

    if products:
        if request.GET.get('sort') == 'newest':
            products = products.order_by('-created_at')
        elif request.GET.get('sort') == 'oldest':
            products = products.order_by('created_at')
        paginator = Paginator(products, 3)
        products, objects2 = paginator.get_page(request.GET.get('page')), PriceRange.objects.all()
        return render(request, 'product/product-list.html', context={'objects':products, 'objects2':objects2})
    return redirect('home:home')