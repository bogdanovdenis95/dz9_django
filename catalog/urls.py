from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import product_detail

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact_page, name='contact'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
