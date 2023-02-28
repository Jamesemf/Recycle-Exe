from os import truncate

from django.shortcuts import render, redirect
from .models import Transaction, Statistic, BinData
import webbrowser
import geopy.distance


# Create your views here.
def getTransactions(request):
    # If user not login, redirect them to login page.
    if not request.user.is_authenticated:
        return redirect('login')

    # When user press the 'scan it!' button, check if they are within range.
    data = Transaction.objects.all()

    if request.method == 'POST':
        distance, closeBin = withinRange(request)
        distance = 2
        if distance > 10:
            msg = "You're too far from the bin by", distance, "metres"
            data_dict = {
                'Transaction': data,
                'message': msg
            }
            a_website = "http://maps.google.com/?q=" + str(closeBin[0]) + "," + str(closeBin[1])
            webbrowser.open_new_tab(a_website)
            return render(request, 'home/index.html', data_dict)
        else:
            return redirect('barcode_lookup')
    else:
        data_dict = {
            'Transaction': data,
            'message': 'Scan Item?'
        }
        return render(request, 'home/index.html', data_dict)
    # Default looking of index.



def getLeaderboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    statData = Statistic.objects.all().order_by('-points')
    data_dict = {
        'Statistics': statData,
    }
    return render(request, 'home/Leaderboard.html', data_dict)


def withinRange(request):
    curr_lat = float(request.POST.get("location_lat"))
    curr_long = float(request.POST.get("location_long"))
    coords_1 = (curr_lat, curr_long)

    shortestDistance = 100000000
    closeBin = None

    for bin in BinData.objects.all():
        coords_2 = (bin.binLat, bin.binLong)
        distance = geopy.distance.geodesic(coords_1, coords_2).m
        if distance < shortestDistance:
            shortestDistance = distance
            closeBin = coords_2

    return shortestDistance, closeBin

