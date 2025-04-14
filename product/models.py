from django.db import models
from account.models import User
from django.urls import reverse
from django.utils.text import slugify

class Brand(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title
class PriceRange(models.Model):
    a_price = models.SmallIntegerField()
    b_price = models.SmallIntegerField()
    def __str__(self):
        return f"{self.a_price} to {self.b_price}"
class Category(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title
class Size(models.Model):
    title = models.CharField(max_length=10)
    def __str__(self):
        return self.title
class Color(models.Model):
    title = models.CharField(max_length=10)
    def __str__(self):
        return self.title
class Product(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True,)
    title = models.CharField(max_length=255)
    description =models.TextField()
    price = models.IntegerField()
    discount = models.SmallIntegerField()
    price_range = models.ForeignKey(PriceRange, related_name='pricerange', on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='brand', blank=True, on_delete=models.CASCADE, null=True)
    category = models.ManyToManyField(Category, related_name='category', blank=True)
    size = models.ManyToManyField(Size, related_name='size', blank=True)
    color = models.ManyToManyField(Color, related_name='color', blank=True)
    is_trend = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def discount_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price

    def get_absolute_url(self):
        return reverse('product:detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} {self.description[:50]}...'

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='products_images')


class Information(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='informations',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    text = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.text[:30]}..."

class ProductComment(models.Model):
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    product = models.ForeignKey(Product, related_name='comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} -> {self.body[:70]}...'

