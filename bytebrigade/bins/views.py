from django.shortcuts import render, redirect
from .models import BinData

# Create your views here.
def bin_map_view(request):
    print(request.session['newHome'])
    if request.method == 'POST':
        # Take me to the bin nav thing
        return redirect('recycle_confirm')
    if request.session['newHome'] != -1:
        data_dict = {
            'bin': BinData.objects.get(binId=request.session['newHome']),
            'presentButton': 1,
        }
    else:
        data_dict = {
            'bins': BinData.objects.all(),
            'presentButton': 0
        }

    return render(request, 'bin_map.html', data_dict)


def bin_nav_view(request):
    return render(request, 'bin_nav.html')


def bin_arrived_view(request):
    return render(request, 'bin_arrived.html')


# def bin_map(request):
#     # bin_general = models.BooleanField(default=False)
#     # bin_recycle = models.BooleanField(default=False)
#     # bin_paper = models.BooleanField(default=False)
#     # bin_cans = models.BooleanField(default=False)
#     # bin_glass = models.BooleanField(default=False)
#     # bin_plastic = models.BooleanField(default=False)
#     # bin_non_rec = models.BooleanField(default=False)
#
#     data = BinData.objects.all()
#
#     data_dict = {'Bins': data, 'presentButton': 0}
#
#     return render(request, 'bin_map.html', data_dict)
