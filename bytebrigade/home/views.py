from django.shortcuts import render, redirect
from home.models import Transaction
from account.models import Statistic
from bins.models import BinData
import geopy.distance

# function for the home page backend
def home_view(request):
    # If user not login, redirect them to login page.
    request.session['barcode'] = -1  # The barcode that the user has scanned
    request.session['newHome'] = -1  # The closest bin
    request.session['valid'] = -1  # If the user has scanned a product, they are valid for the scanner page
    if not request.user.is_authenticated:
        return redirect('login')
    data = Transaction.objects.all()[:5]
    data_dict = {
        'Transaction': data
    }
    if request.method == 'POST':
        # If they want to go to scan an item then we redirect them.
        return redirect('barcode_lookup')
    # Return normal feed page
    return render(request, 'home/index.html', data_dict)


# Handles a request for the leaderboard page, ordering the users by their points
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


# Function that checks you are within the minimum range of a bin and return's information about your closest bin
def withinRange(request, binType):
    curr_lat = float(request.POST.get("location_lat"))
    curr_long = float(request.POST.get("location_long"))
    coords_1 = (curr_lat, curr_long)

    shortestDistance = 100000000
    close_bin = None
    bin_object = None

    for bin in BinData.objects.all():
        coords_2 = (bin.binLat, bin.binLong)
        distance = geopy.distance.geodesic(coords_1, coords_2).m
        if distance < shortestDistance:
            if bin.bin_general and (binType == 'General'):
                shortestDistance = distance
                close_bin = coords_2
                bin_object = bin
            if bin.bin_paper and (binType == 'Paper'):
                shortestDistance = distance
                close_bin = coords_2
                bin_object = bin
            if bin.bin_cans and (binType == 'Cans'):
                shortestDistance = distance
                close_bin = coords_2
                bin_object = bin
            if bin.bin_glass and (binType == 'Glass'):
                shortestDistance = distance
                close_bin = coords_2
                bin_object = bin
            if bin.bin_plastic and (binType == 'Plastic'):
                shortestDistance = distance
                close_bin = coords_2
                bin_object = bin
    return shortestDistance, close_bin, bin_object


