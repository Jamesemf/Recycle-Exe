from django.db import models


class BinData(models.Model):
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
