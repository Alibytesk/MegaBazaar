from django.urls import path
from product import views

app_name = 'product'
urlpatterns = [
    path('items', views.products_list, name='items'),
    path('<slug:slug>', views.detail, name='detail'),
    path('like/<slug:slug>/<int:id>', views.like, name='like')
]