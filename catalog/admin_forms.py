# catalog/admin_forms.py
from django import forms
from .models import Product

class AdminProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
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
