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
    return render(request, 'home/Leaderboard.html')
