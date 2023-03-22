from django.shortcuts import render, redirect
from .models import BinData
import geopy.distance
from home.views import reset_sessions


def bin_map_view(request):
    """
    Web backend for '../bin/map/' (name 'bin_map')

    This function handles POST and GET requests.
    If the request method is POST then the user is redirected to the recycle confirm
    page.
    If the request method is GET and the 'newHome' session variable is set then the
    bin object with the same id as the session variable is added to data_dict. If the
    session variable is not set then all bin objects are retrieves and added to the
    data_dict. A render is then sent to 'bin_map.html' containing the data_dict
    """
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        return redirect('bin_nav')

    if request.session['shownMap'] != -1:
        if request.session['newHome'] != -1:
            data_dict = {
                'bin': BinData.objects.get(binId=request.session['newHome']),
                'presentButton': 1,
            }
        request.session['shownMap'] = -1
    else:
        reset_sessions(request)
        data_dict = {
            'Bins': BinData.objects.all(),
            'presentButton': 0
        }

    return render(request, 'bin_map.html', data_dict)


def bin_nav_view(request):
    """
    Web backend for '../bin/nav/' (name 'bin_nav')

    This function returns a render to 'bin_nav.html'

    Feed into this the lat and long of where to point
    Current meters
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        request.session['success_recycle'] = 1
        return redirect('recycle_confirm')
    if request.session['newHome'] != -1:
        data_dict = {'BinGoal': BinData.objects.get(binId=request.session['newHome'])}
        return render(request, 'bin_nav.html', data_dict)
    else:
        return redirect('bin_map')


def binDistance(request, binGoal):
    """
    This function calculates the distance between you and the bin goal.

    Parameters:
        binGoal: The bin which you aim to go to

    Returns:
        distance: The distance between you and the bin
    """

    curr_lat = float(request.POST.get("location_lat"))
    curr_long = float(request.POST.get("location_long"))
    coords_1 = (curr_lat, curr_long)

    coords_2 = (binGoal.binLat, binGoal.binLong)
    distance = geopy.distance.geodesic(coords_1, coords_2).m
    return distance


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