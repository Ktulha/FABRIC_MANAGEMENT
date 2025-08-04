from django import forms

from sales.models import Product


class ProductEdit(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
