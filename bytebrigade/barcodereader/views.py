from django.shortcuts import render
from django.http import HttpResponse
from home.models import BinData
import webbrowser
import geopy.distance


def barcode_lookup(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
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

        if shortestDistance < 1:
            data_dict = {"nearBin": True}
            return render(request, 'BCscanner/Scanner_page.html', data_dict)

        else:
            data_dict = {"nearBin": False}
            a_website = "http://maps.google.com/?q=" + str(closeBin[0]) + "," + str(closeBin[1])
            webbrowser.open_new_tab(a_website)
            return render(request, 'BCscanner/Scanner_page.html', data_dict)

    else:
        return render(request, 'BCscanner/Scanner_page.html')
