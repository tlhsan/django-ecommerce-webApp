from django.urls import path
from .import views

urlpatterns = [
    path('', views.storeView, name = 'store'),
    path('cart/', views.cartView, name = 'cart'),
    path('checkout/', views.checkoutView, name = 'checkout'),
    path('update-item/', views.updateItem, name = 'update-item'),
]
