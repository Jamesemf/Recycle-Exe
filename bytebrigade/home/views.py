from django.shortcuts import render, redirect
from .models import Transaction, Statistic, BinData
import webbrowser
import geopy.distance


"""
def getTransactions(request):
    # If user not login, redirect them to login page.
    request.session['barcode'] = -1
    if not request.user.is_authenticated:
        return redirect('login')

    data = Transaction.objects.all()[:5]

    # Called when a user clicks to scan an item
    if request.method == 'POST':
        distance, close_bin, bin_object = withinRange(request)
        x = round(distance)
        request.session['bin_data'] = bin_object.binId
        #distance = 2
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
            return render(request, 'home/index.html', data_dict)  # if the user is out of range, give directions

        else:
            return redirect('barcode_lookup')  # If the user is within range redirect to scanner page
    else:
        data_dict = {
            'Transaction': data
        }
        #Return normal feed page
        return render(request, 'home/index.html', data_dict)
    # Default looking of index.
"""


# function for the home page backend
def home_view(request):
    # If user not login, redirect them to login page.
    request.session['barcode'] = -1
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
def withinRange(request):
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
            if bin.bin_general and (request.session['newHome'] == 'General'):
                shortestDistance = distance
                close_bin = coords_2
                bin_object = bin
            if bin.bin_paper and (request.session['newHome'] == 'Paper'):
                shortestDistance = distance
                close_bin = coords_2
                bin_object = bin
            if bin.bin_cans and (request.session['newHome'] == 'Cans'):
                shortestDistance = distance
                close_bin = coords_2
                bin_object = bin
            if bin.bin_glass and (request.session['newHome'] == 'Glass'):
                shortestDistance = distance
                close_bin = coords_2
                bin_object = bin
            if bin.bin_plastic and (request.session['newHome'] == 'Plastic'):
                shortestDistance = distance
                close_bin = coords_2
                bin_object = bin
    return shortestDistance, close_bin, bin_object


