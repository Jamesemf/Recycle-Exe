from django.shortcuts import render, redirect
from .models import BinData


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
        # return redirect(bin_nav)
        return redirect('recycle_confirm')

    if request.session['newHome'] != -1:
        data_dict = {
            'Bins': BinData.objects.get(binId=request.session['newHome']),
            'presentButton': 1,
        }
    else:
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
        return redirect('recycle_confirm')

    data_dict = {'BinGoal': BinData.objects.get(binId=request.session['newHome']),}
    return render(request, 'bin_nav.html', data_dict)


# Potentially might want to remove this as could make recycle confirm the bin arrived view instead
def bin_arrived_view(request):
    """
    Web backend for '../bin/arrived/' (name 'bin_arrive')

    This function returns a render to the 'bin_arrived.html'
    """
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'bin_arrived.html')


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

# Could use this instead on the webpage and constantly refresh it
# Once the js has a distance of less than 1m then we submit a post request which will lead to bin arrived view
# var haversine = require("haversine-distance");
#
# //First point in your haversine calculation
# var point1 = { lat: 6.1754, lng: 106.8272 }
#
# //Second point in your haversine calculation
# var point2 = { lat: 6.1352, lng: 106.8133 }
#
# var haversine_m = haversine(point1, point2); //Results in meters (default)
# var haversine_km = haversine_m /1000; //Results in kilometers
#
# console.log("distance (in meters): " + haversine_m + "m");
# console.log("distance (in kilometers): " + haversine_km + "km");
