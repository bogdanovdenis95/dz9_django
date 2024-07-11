from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Product


class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        context = {
            'products': products,
        }
        return render(request, 'home.html', context)


class ContactView(TemplateView):
    template_name = 'contacts.html'


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        context = {'product': product}
        return render(request, 'product_detail.html', context)
