from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=16, min_length=4,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', max_length=255, min_length=8,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
