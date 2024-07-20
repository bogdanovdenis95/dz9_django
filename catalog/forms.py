# catalog/forms.py
from django import forms
from .models import Product, Version
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in prohibited_words:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"Запрещенное слово в названии: {word}")
        return name
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in prohibited_words:
            if word.lower() in description.lower():
                raise forms.ValidationError(f"Запрещенное слово в описании: {word}")
        return description

class VersionForm(forms.ModelForm):
    delete_version = forms.BooleanField(required=False, label='Удалить версию')

    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_current', 'delete_version']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.layout = Layout(
            Row(
                Column('version_number', css_class='form-group col-md-6 mb-0'),
                Column('version_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'is_current',
            'delete_version',
            Submit('submit', 'Save')
        )

        self.fields['is_current'].widget.attrs.update({'class': 'form-check-input'})
    
    def save(self, commit=True, product=None):
        version_number = self.cleaned_data['version_number']
        if product:
            try:
                version = Version.objects.get(product=product, version_number=version_number)
                version.version_name = self.cleaned_data['version_name']
                version.is_current = self.cleaned_data['is_current']
                if commit:
                    version.save()
                return version
            except Version.DoesNotExist:
                pass
        
        instance = super().save(commit=False)
        if product:
            instance.product = product
        if commit:
            instance.save()
        return instance
    
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')