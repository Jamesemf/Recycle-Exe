from django.shortcuts import render
from .models import Transactions
from .models import Statistics
from django.http import HttpResponse


# Create your views here.

def getTransactions(request):
    data = Transactions.objects.all()
    data_dict = {
        'Transactions': data,
    }

    return render(request, 'home/index.html', data_dict)


def getLeaderboard(request):

    statData = Statistics.objects.all().order_by('-points')
    data_dict = {
        'Statistics': statData,
    }

    return render(request, 'home/Leaderboard.html', data_dict)
