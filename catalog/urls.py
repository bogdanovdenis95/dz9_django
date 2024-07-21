from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    HomeView, ContactView, ProductDetailView, ProductCreateView, 
    ProductUpdateView, ProductDeleteView, ProductListView, 
    CategoryListView, change_product_description, change_product_category, 
    unpublish_product, SignUpView
)

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('product/<int:pk>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('product/<int:product_id>/change_description/', change_product_description, name='change_product_description'),
    path('product/<int:product_id>/change_category/', change_product_category, name='change_product_category'),
    path('product/<int:product_id>/unpublish/', unpublish_product, name='unpublish_product'),
    path('register/', SignUpView.as_view(), name='register'),
]
