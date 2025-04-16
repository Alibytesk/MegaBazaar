from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.http import Http404
from django.contrib.auth import mixins
from django.utils.crypto import get_random_string
from django.urls import reverse
from account.models import Address
from cart.models import Cart, Order, OrderObject
from django.contrib import messages
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

class ApplyCouponView(View):

    def post(self, request):
        code = request.POST.get('code')
        cart = Cart(request)
        if cart.apply__coupon(code):
            messages.success(request, 'applied Coupon Code')
        else:
            messages.success(request, 'Coupon Code is InValid')
        return redirect('cart:cart')

class DeleteFromCartView(View):

    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect("cart:cart")

class OrderDetailView(mixins.LoginRequiredMixin, View):

    def get(self, request, pk):
        if Order.objects.filter(token=request.GET.get('token'), user_id=request.user.id).exists():
            order = get_object_or_404(Order, pk=pk)
            return render(request, 'cart/checkout.html', context={'order':order})
        else:
            raise Http404('go fuck yourself kid')

class OrderCreationView(mixins.LoginRequiredMixin, View):

    def get(self, request):
        cart, token = Cart(request), get_random_string(length=255)
        order = Order.objects.create(user=request.user, pay_price=cart.get_total_price_after_discount(), token=token)
        for item in cart:
            OrderObject.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
                color=item['color'],
                size=item['size']
            )
        cart.remove_cart()
        return redirect(reverse('cart:order_detail', kwargs={'pk':order.pk}) + f"?token={token}")

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