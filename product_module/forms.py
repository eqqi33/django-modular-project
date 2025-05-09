# forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'barcode', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:ring-primary-500 focus:border-primary-500 text-sm py-2 px-3',
                'placeholder': 'Enter product name'
            }),
            'barcode': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:ring-primary-500 focus:border-primary-500 text-sm py-2 px-3',
                'placeholder': 'Enter barcode'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:ring-primary-500 focus:border-primary-500 text-sm py-2 px-3',
                'placeholder': 'Enter price'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:ring-primary-500 focus:border-primary-500 text-sm py-2 px-3',
                'placeholder': 'Enter stock quantity'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.label_suffix = ' *'