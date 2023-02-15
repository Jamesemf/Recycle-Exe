from django.shortcuts import render
from .models import Transactions
from django.http import HttpResponse
# Create your views here.

def getTransactions(request):
    query_results = Transactions.objects.all()
    return render(request, 'home/index.html', query_results)