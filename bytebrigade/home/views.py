from django.shortcuts import render, redirect
from .models import Transaction, Statistic
from django.contrib.auth import authenticate, login

# Create your views here.

def getTransactions(request):
    if not request.user.is_authenticated:
        return redirect('login')

    data = Transaction.objects.all()
    data_dict = {
        'Transaction': data,
    }
    return render(request, 'home/index.html', data_dict)


def getLeaderboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    statData = Statistic.objects.all().order_by('-points')
    data_dict = {
        'Statistics': statData,
    }
    return render(request, 'home/Leaderboard.html', data_dict)
