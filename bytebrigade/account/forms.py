from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    """
        Registration Form (for registration page)
        Inheritance from django default user models (username, email) and added password and password_confirm.
        Defined validation function for checking whether the two password are the same.
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'minlength': 8}))
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'minlength': 8}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def confirm_password(self):
        """
            Validation function that ensure the password and the confirmed one are the same.
        """
        cleandata = self.cleaned_data
        if cleandata['password'] != cleandata['password_confirm']:
            raise forms.ValidationError('Password do not match!')
        else:
            return cleandata['password_confirm']


