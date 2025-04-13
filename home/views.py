from django.shortcuts import render
from django.views.generic.base import View
from product.models import Product


class HomeView(View):

    def get(self, request):
        return render(request, 'home/index.html', context={
            "objects1":Product.objects.all()
        })
