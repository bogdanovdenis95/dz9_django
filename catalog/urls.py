from django.urls import path
from .views import (
    HomeView, ContactView, ProductDetailView, ProductCreateView, ProductUpdateView, 
    ProductDeleteView, change_product_description, change_product_category, unpublish_product
)

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:product_id>/change_description/', change_product_description, name='change_product_description'),
    path('product/<int:product_id>/change_category/', change_product_category, name='change_product_category'),
    path('product/<int:product_id>/unpublish/', unpublish_product, name='unpublish_product'),
]
