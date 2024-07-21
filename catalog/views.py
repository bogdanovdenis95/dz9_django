# catalog/views.py
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from .models import Product, Version, Category
from .forms import ProductForm, VersionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .services import get_categories

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
        
        # Добавляем информацию о праве редактирования и удаления
        user = self.request.user
        if user.is_authenticated:
            context['can_edit_or_delete'] = user.groups.filter(name='Moderator').exists()
        else:
            context['can_edit_or_delete'] = False

        return context


class ContactView(TemplateView):
    template_name = 'contacts.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'

    @method_decorator(cache_page(60 * 15))  # Кэширование на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Получение активной версии для текущего продукта
        active_version = Version.objects.filter(product=product, is_current=True).first()
        
        context['active_version'] = active_version
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_superuser and not request.user.groups.filter(name='Moderator').exists():
            if self.object.owner != request.user:
                return HttpResponseForbidden("У вас нет прав доступа к редактированию этого продукта.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['version_form'] = VersionForm(self.request.POST)
        else:
            product = self.get_object()
            version = product.version_set.first()
            if version:
                initial_data = {
                    'version_number': version.version_number,
                    'version_name': version.version_name,
                    'is_current': version.is_current,
                }
                context['version_form'] = VersionForm(initial=initial_data)
            else:
                context['version_form'] = VersionForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        version_form = context['version_form']
        if version_form.is_valid():
            self.object = form.save()
            version = self.object.version_set.filter(version_number=version_form.cleaned_data['version_number']).first()
            if version_form.cleaned_data['delete_version']:
                if version:
                    version.delete()
            else:
                version_form.save(commit=True, product=self.object)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_superuser and not request.user.groups.filter(name='Moderator').exists():
            if self.object.owner != request.user:
                return HttpResponseForbidden("У вас нет прав доступа к удалению этого продукта.")
        return super().dispatch(request, *args, **kwargs)


class ProductListView(LoginRequiredMixin, ListView):
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
            active_version = product.version_set.filter(is_current=True).first()
            if active_version:
                active_versions[product.id] = active_version

        # Добавляем словарь активных версий в контекст
        context['active_versions'] = active_versions
        return context


@login_required
def change_product_description(request, product_id):
    if not request.user.has_perm('catalog.change_description'):
        return HttpResponseForbidden("У вас нет разрешения на изменение описания продукта.")
    
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        new_description = request.POST.get('description')
        product.description = new_description
        product.save()
        return redirect('catalog:product_detail', pk=product.id)

    return render(request, 'catalog/change_product_description.html', {'product': product})


@login_required
def change_product_category(request, product_id):
    if not request.user.has_perm('catalog.change_category'):
        return HttpResponseForbidden("У вас нет разрешения на изменение категории продукта.")
    
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    if request.method == "POST":
        new_category_id = request.POST.get('category')
        new_category = get_object_or_404(Category, id=new_category_id)
        product.category = new_category
        product.save()
        return redirect('catalog:product_detail', pk=product.id)

    return render(request, 'catalog/change_product_category.html', {'product': product, 'categories': categories})


@login_required
def unpublish_product(request, product_id):
    if not request.user.has_perm('catalog.off_published'):
        return HttpResponseForbidden("У вас нет разрешения на отмену публикации продукта.")
    
    product = get_object_or_404(Product, id=product_id)
    product.is_published = False
    product.save()
    return redirect('catalog:product_detail', pk=product.id)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class CategoryListView(ListView):
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        # Получаем категории через сервисную функцию с кешированием
        return get_categories()