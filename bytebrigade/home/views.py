from django.shortcuts import render
from .models import Transaction, Statistic

# Create your views here.

def getTransactions(request):
    data = Transaction.objects.all()
    data_dict = {
        'Transaction': data,
    }
    return render(request, 'home/index.html', data_dict)


def getLeaderboard(request):

    statData = Statistic.objects.all().order_by('-points')
    data_dict = {
        'Statistic': statData,
    }

    return render(request, 'home/Leaderboard.html', data_dict)
