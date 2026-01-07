from django.urls import path
from .views import ProductListView, CartView, CheckoutView, OrderView, CategoryListView, ReviewView

urlpatterns = [
    # Define your shop-related URL patterns here
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('reviews/', ReviewView.as_view(), name='reviews'),
]