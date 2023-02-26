from django.shortcuts import render
from .models import Transaction, Statistic, BinData
from django.http import HttpResponse
import math

# Create your views here.


def getTransactions(request):
    if request.method == "POST":
        curr_lat = float(request.POST.get("location_lat"))
        curr_long = float(request.POST.get("location_long"))

        R = 6371
        shortest_distance = 100000000000
        for bin in BinData.objects.all():
            dLat = (float(bin.binLat) - curr_lat) * (math.pi / 180)
            dLon = (float(bin.binLong) - curr_long) * (math.pi / 180)
            a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(curr_lat * (math.pi / 180)) * math.cos(curr_long * (math.pi / 180)) * math.sin(dLon / 2) * math.sin(dLon / 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = 1000 * R * c
            if distance < shortest_distance:
                shortest_distance = distance

        print(shortest_distance)

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
