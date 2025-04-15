from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth import mixins
from cart.models import Cart
from product.models import Product


class CartView(View):
    template_name = 'cart/cart.html'
    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, context={'cart':cart})

class AddToCartView(View):

    def post(self, request, pk):
        product, quantity, size, color = (
            get_object_or_404(Product, pk=pk),
            request.POST.get('quantity'),
            request.POST.get('size'),
            request.POST.get('color')
        )
        cart = Cart(request)
        cart.add(product, quantity, size, color)
        return redirect('product:detail', product.slug)

class DeleteFromCartView(View):

    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect("cart:cart")


class CartCounterView(View):
    """
    with django-render-partial
    includes_template: includes/bottom_bar.html
    base: base/base.html
    url_name: cart_counter
    """
    def get(self, request):
        cart = Cart(request)
        return render(request, 'includes/bottom_bar.html', context={
            'cart_counter':len(cart.cart)
        })