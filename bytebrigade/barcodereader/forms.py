from django import forms

class barcode_form(forms.ModelForm):
    type = forms.CharField()
    barcode = forms.CharFieldforms.CharField()

class product_form(forms.ModelForm):
    title = forms.CharField()
    images = forms.ImageField()
    material = forms.CharField()
    weight = forms.DecimalField()
    barcode = forms.IntegerField()



