from django.urls import path
from .views import *

urlpatterns = [
    # Product URLs
    path('products/all/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    path('products/create/', ProductViewSet.as_view({'post': 'create'}), name='product-create'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
    path('products/<int:pk>/update/', ProductViewSet.as_view({'put': 'update'}), name='product-update'),
    path('products/<int:pk>/delete/', ProductViewSet.as_view({'delete': 'destroy'}), name='product-delete'),

    # Cart URLs
    path('carts/current/', CartViewSet.as_view({'get': 'retrieve'}), name='cart-detail'),
    path('carts/create/', CartViewSet.as_view({'post': 'create'}), name='cart-create'),
    path('carts/<int:pk>/delete/', CartViewSet.as_view({'delete': 'destroy'}), name='cart-delete'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),

    path('pay/', PayCartView.as_view(), name='pay-cart'),
]