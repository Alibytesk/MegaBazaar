from django.shortcuts import render
from django.views.generic.base import View
from product.models import Product, Category


class HomeView(View):

    def get(self, request):
        return render(request, 'home/index.html', context={
            "objects1":Product.objects.all(),
            'objects2':Category.objects.all(),
            'objects3':Product.objects.filter(is_up=True)
        })
