from django.shortcuts import render, redirect
from home.models import Transaction
from account.models import Statistic
from bins.models import BinData
from products.models import Product
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
    request.session['pokedex_barcode'] = -1
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        return redirect('barcode_lookup')   # Redirect to the scanner page
    if BinData.objects.count() == 0:
        bins = [['FORUM-MAIN-OUT', 'Forum main entrance Outside', 50.735666895923100001, -3.533641953682420000, True, True, True, True, True, True, False, False],
                ['IN-1-SWIOT-1', 'Innovation 1 SWIOT 1', 50.737929365592700001, -3.530370602541640000, False, False, False, True, False, True, True, False],
                ['INTO-OUT', 'INTO Outside carpark', 50.7359469093508000018, -3.534357688043370000, True, False, False, True, False, True, True, False],
                ['LAF-MAB', 'Lafrowda MA MB Bin shed', 50.734501000805200001, -3.527055005716390000, True, True, True, True, True, True, False, False],
                ['ROWE', 'Rowe House Bin shed', 50.734291038584400001, -3.528512745930170000, True, True, True, True, True, True, False, False],
                ['XFI-LEC', 'XFI Building Lecture', 50.735844192079400001, -3.529726038441900000, True, False, False, True, False, True, False, False]]
        for item in bins:
            print(item)
            bin_ob = BinData(binId=item[0], binName=item[1], binLat=item[2], binLong=item[3], binPhoto='figures/bins/default.jpg', bin_general=item[4], bin_recycle=item[5], bin_paper=item[6], bin_cans=item[7], bin_glass=item[8], bin_plastic=item[9], bin_non_rec=item[10])
            print(bin_ob)
            bin_ob.save()

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


