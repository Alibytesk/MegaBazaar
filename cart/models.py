from django.db import models
from product import models as BaseProductModels
from django.utils import timezone

class Cart:

    def __new__(cls, *args, **kwargs):
        return super(Cart, cls).__new__(cls)

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = dict()
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def __iter__(self):
        cart = self.cart.copy()
        for i in cart.values():
            product = BaseProductModels.Product.objects.get(id=int(i['id']))
            i['product'] = product
            i['total'] = (int(i['quantity']) * int(i['price']))
            i['uniqueid'] = self._unique_id_generator(product.id, i['color'], i['size'])
            if 0 < float(i['discount']) and 'discount' in i:
                i['per_total_price'] = float(
                    float(i['total']) - ((float(i['discount']) * float(i['quantity']))  * float(i['price']) * float(i['quantity']) / 100 )
                )
            else:
                i['per_total_price'] = i['total']
            yield i

    def add(self, product, quantity, color, size):
        unique = self._unique_id_generator(product.id, color, size)
        if unique not in self.cart:
            self.cart[unique] = dict({
                'id': str(product.id),
                'quantity': int(),
                'price': str(product.price),
                'discount': str(product.discount if hasattr(product, 'discount') else int()),
                'color': color,
                'size': size
            })
        self.cart[unique]['quantity'] += int(quantity)
        self.save()

    def apply__coupon(self, code):
        try:
            coupon = CouponCode.objects.get(code__iexact=code)
            if coupon.is_valid():
                self.session['coupon_id'] = self.coupon_id = coupon.id
                self.save()
                return True
        except CouponCode.DoesNotExist:
            pass
        return False

    def get_discount(self):
        if self.coupon_id:
            try:
                coupon = CouponCode.objects.get(id=self.coupon_id)
                if coupon.is_valid():
                    return (coupon.discount / 100) * self.sum_total_price()
            except CouponCode.DoesNotExist:
                pass
        return 0

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def sum_total_price(self):
        return round(sum(i['per_total_price'] for i in self), 2) + 7

    def get_total_price_after_discount(self):
        return self.sum_total_price() - self.get_discount()

    def _unique_id_generator(self, id, color, size):
        return f"{id}{color}{size}"

    def save(self):
        self.session.modified = True


class CouponCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    start_valid = models.DateTimeField()
    expire_valid = models.DateTimeField()

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_valid <= now <= self.expire_valid

    def __str__(self):
        return f"{self.code} | {self.discount}"