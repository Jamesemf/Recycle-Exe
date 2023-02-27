from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
from home.models import Statistic


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            # New user object without saving
            new_user = user_form.save(commit=False)
            # Set password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_statistic = Statistic.objects.create(user=new_user)
            new_statistic.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = RegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def account(request):
    if request.user.is_authenticated:
        data = Statistic.objects.get(user=request.user)
        maxWeek = Statistic.objects.all().order_by('curweek')[0]
        maxMonth = Statistic.objects.all().order_by('curmonth')[0]
        maxYear = Statistic.objects.all().order_by('curyear')[0]

        data_dict = {
            'Profile': data,
            'maxWeek': maxWeek,
            'maxMonth': maxMonth,
            'maxYear': maxYear,
        }
        return render(request, 'account/Profile_page.html', data_dict)
    else:
        return redirect('login')

def password(request):
    return render(request, 'account/password.html')


