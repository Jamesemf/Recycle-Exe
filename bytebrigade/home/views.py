from django.shortcuts import render
from .models import Transactions
from django.http import HttpResponse


# Create your views here.

def getTransactions(request):
    data = Transactions.objects.all()
    data_dict = {
        'Transaction': data
    }
    return render(request, 'home/index.html', data_dict)
