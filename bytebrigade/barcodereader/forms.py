from django import forms
from home.models import Product


class barcode_form(forms.Form):
    type = forms.CharField()
    barcode = forms.CharField()
