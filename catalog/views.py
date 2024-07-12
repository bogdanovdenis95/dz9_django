# catalog/views.py
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Product, Version
from .forms import ProductForm, VersionForm

class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем все продукты
        products = Product.objects.all()
        
        # Создаем пустой словарь для хранения активных версий продуктов
        active_versions = {}

        # Перебираем каждый продукт
        for product in products:
            # Находим активную версию для данного продукта
            active_version = Version.objects.filter(product=product, is_current=True).first()
            if active_version:
                active_versions[product.id] = active_version

        # Добавляем словарь активных версий в контекст
        context['active_versions'] = active_versions
        return context


class ContactView(TemplateView):
    template_name = 'contacts.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Получение активной версии для текущего продукта
        active_version = Version.objects.filter(product=product, is_current=True).first()
        
        context['active_version'] = active_version
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['version_form'] = VersionForm(self.request.POST, instance=self.object)
        else:
            context['version_form'] = VersionForm(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        version_form = context['version_form']
        if version_form.is_valid():
            self.object = form.save()
            version_data = version_form.cleaned_data
            delete_version = version_data.pop('delete_version', False)
            if delete_version:
                version_number = version_data.get('version_number')
                Version.objects.filter(product=self.object, version_number=version_number).delete()
            else:
                version_data['product'] = self.object
                Version.objects.update_or_create(product=self.object, version_number=version_data['version_number'], defaults=version_data)
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем все продукты
        products = Product.objects.all()
        
        # Создаем пустой словарь для хранения активных версий продуктов
        active_versions = {}

        # Перебираем каждый продукт
        for product in products:
            # Находим активную версию для данного продукта
            active_version = product.versions.filter(is_current=True).first()
            if active_version:
                active_versions[product.id] = active_version

        # Добавляем словарь активных версий в контекст
        context['active_versions'] = active_versions
        return context
    
def version_form_view(request):
    if request.method == 'POST':
        form = VersionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete_version']:
                # Удаление версии
                version_number = form.cleaned_data['version_number']
                Version.objects.filter(version_number=version_number).delete()
            else:
                form.save()
            return redirect('success_url')  # Укажите URL для перенаправления после успешного сохранения
    else:
        form = VersionForm()
    
    return render(request, 'version_form.html', {'form': form})

def product_form_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = VersionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_detail', pk=product.pk)  # Перенаправление на детали продукта или другой URL
    else:
        form = VersionForm(initial={'product': product})
    
    context = {
        'view': {'title': 'Редактирование товара'},
        'version_form': form,
    }
    return render(request, 'product_form.html', context)