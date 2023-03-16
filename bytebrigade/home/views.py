from django.shortcuts import render, redirect
from home.models import Transaction
from account.models import Statistic
from bins.models import BinData
import geopy.distance

# function for the home page backend
def home_view(request):
    """
    Web backend for '../' (name 'index')

    This function intialises / resets session variables and handles POST and GET requests.
    If the request is a GET, then the function retrieves the first 5 entries from the transaction
    model and returns a render to 'index.html' passing a data_dict with the latest transaction
    information.
    If the request is a POST then the user is redirected to the scanner page.
    """
    request.session['barcode'] = -1  # The barcode that the user has scanned
    request.session['newHome'] = -1  # The closest bin
    request.session['valid'] = -1  # If the user has scanned a product, they are valid for the scanner page

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        return redirect('barcode_lookup')   # Redirect to the scanner page

    data = Transaction.objects.all().order_by('-time')[:5]
    data_dict = {
        'Transaction': data
    }

    return render(request, 'home/index.html', data_dict) #  Return index page


# Handles a request for the leaderboard page, ordering the users by their points
def getLeaderboard(request):
    """
    Web backend for '../leaderboard/' (name 'leaderboard')

    This function retrieves all entries from the statistic model ordered by the points
    value in the model. It then returns a render of 'Leaderboard.html' passing the data_dict
    with the model information.
    """

    if not request.user.is_authenticated:
        return redirect('login')  #  Redirects to login page if not logged in
    statData = Statistic.objects.all().order_by('-points')
    data_dict = {
        'Statistics': statData,
    }
    return render(request, 'home/Leaderboard.html', data_dict)


def instruction_view(request):
    """
    Web backend for '../abouts/' (name 'instruction')
    Returns:
        * The instruction about page.
    """
    return render(request, 'home/about-me.html')


# Function that checks you are within the minimum range of a bin and return's information about your closest bin
def withinRange(request, binType):
    """
    This function calculates the distance of the closest bin of a particular type.

    Parameters:
        binType: The type of bin to be found

    Returns:
        shortestDistance: the shortest distance
        close_bin: the longitude and latitude of the closest bin
        bin_object: the closest bin_object that fits the binType requirements
    """

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


