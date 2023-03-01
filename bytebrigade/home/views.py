from os import truncate
from django.shortcuts import render, redirect
from .models import Transaction, Statistic, BinData
from django.contrib.auth import authenticate, login
import webbrowser
import geopy.distance

# Create your views here.
def getTransactions(request):
    # If user not login, redirect them to login page.
    request.session['barcode'] = -1
    if not request.user.is_authenticated:
        return redirect('login')

    # When user press the 'scan it!' button, check if they are within range.
    data = Transaction.objects.all()

    if request.method == 'POST':
        distance, close_bin, bin_object = withinRange(request)
        x = round(distance)
        request.session['bin_data'] = bin_object.binId
        distance = 2
        if distance > 10:
            data_dict = {
                'Transaction': data,
                'popup': 1,
                'error': 1,
                'Bin': bin_object,
                'Distance': x,
            }
            a_website = "http://maps.google.com/?q=" + str(close_bin[0]) + "," + str(close_bin[1])
            webbrowser.open_new_tab(a_website)
            return render(request, 'home/index.html', data_dict)
        else:
            return redirect('barcode_lookup')
    else:
        data_dict = {
            'Transaction': data
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


def instruction_view(request):
    return render(request, 'home/about-me.html')


def withinRange(request):
    curr_lat = float(request.POST.get("location_lat"))
    curr_long = float(request.POST.get("location_long"))
    coords_1 = (curr_lat, curr_long)

    shortestDistance = 100000000
    closeBin = None
    binObject = None

    for bin in BinData.objects.all():
        coords_2 = (bin.binLat, bin.binLong)
        distance = geopy.distance.geodesic(coords_1, coords_2).m
        if distance < shortestDistance:
            shortestDistance = distance
            close_bin = coords_2
            bin_object = bin

    return shortestDistance, close_bin, bin_object
