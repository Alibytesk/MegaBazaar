from django.db import models
from product import models

class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = dict()
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for i in cart.values():
            product = models.Product.objects.get(id=int(i['id']))
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

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def total(self):
        pass

    def _unique_id_generator(self, id, color, size):
        return f"{id}{color}{size}"

    def save(self):
        self.session.modified = True

