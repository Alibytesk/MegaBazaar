from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('detail/', views.CartView.as_view(), name='cart'),
    path('add/<int:pk>', views.AddToCartView.as_view(), name='add'),
    path('delete/<str:id>', views.DeleteFromCartView.as_view(), name='delete'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/create', views.OrderCreationView.as_view(), name='order_create'),
    path('applycoupon/', views.ApplyCouponView.as_view(), name="applycoupon"),
    path('cart_counter', views.CartCounterView.as_view(), name='cart_counter'),
]