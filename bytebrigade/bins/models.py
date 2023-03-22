from django.db import models


class BinData(models.Model):
    """
    *** BinData Model ***
    Data model that is used to record bin location and recycle type stats.

    Model Fields:
        binId: The unique id of the bin
        binName: The name of the bin (a better description of its location)
        binLat: The latitude of the bin
        binLong: The longitude of the bin
        binPhoto: A photo of the bins location
        bin_general: If the bin has general waste
        bin_recycle: If the bin has recycling waste
        bin_paper: If the bin has paper waste
        bin_cans: If the bin has can waste
        bin_glass: If the bin has glass waste
        bin_plastic: If the bin has plastic waste
        bin_non_rec: If the bin has non recycling waste
    """
    binId = models.CharField(max_length=100, primary_key=True)  # Format AM-01-1 (Building-Floor-BinNo)
    binName = models.CharField(max_length=100, default="bin")
    binLat = models.DecimalField(max_digits=100, decimal_places=22)
    binLong = models.DecimalField(max_digits=100, decimal_places=22)
    binPhoto = models.ImageField(default='figures/bins/default.jpg')
    bin_general = models.BooleanField(default=False)
    bin_recycle = models.BooleanField(default=False)
    bin_paper = models.BooleanField(default=False)
    bin_cans = models.BooleanField(default=False)
    bin_glass = models.BooleanField(default=False)
    bin_plastic = models.BooleanField(default=False)
    bin_non_rec = models.BooleanField(default=False)
