from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            auth = authenticate(request, username=data['username'], password=data["password"])
            if auth is not None:
                # Check user account whether active
                if auth.is_active:
                    login(request, auth)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login Information')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def account(request):
    return render(request, 'account/account.html')


def password(request):
    return render(request, 'account/password.html')


