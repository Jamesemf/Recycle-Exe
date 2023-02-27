from django import forms
from home.models import Product


class barcode_form(forms.ModelForm):
    type = forms.CharField()
    barcode = forms.CharField()


class product_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('barcode', 'name', 'image', 'type', 'weight', 'category')