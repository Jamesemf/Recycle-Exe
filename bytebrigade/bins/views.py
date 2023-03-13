from django.shortcuts import render
from bins.models import BinData

# Create your views here.

def bin_map(request):
    # bin_general = models.BooleanField(default=False)
    # bin_recycle = models.BooleanField(default=False)
    # bin_paper = models.BooleanField(default=False)
    # bin_cans = models.BooleanField(default=False)
    # bin_glass = models.BooleanField(default=False)
    # bin_plastic = models.BooleanField(default=False)
    # bin_non_rec = models.BooleanField(default=False)

    data = BinData.objects.all()

    data_dict = {'Bins': data}

    return render(request, 'BCscanner/bin_map.html', data_dict)
