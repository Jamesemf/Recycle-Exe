from django.db import models
from django.contrib.auth.models import User
import time
# Create your models here.
class BinData(models.Model):
    binId = models.CharField(max_length=10, primary_key=True)  # Format AM-01-1 (Building-Floor-BinNo)
    binLat = models.DecimalField(max_digits=25, decimal_places=22)
    binLong = models.DecimalField(max_digits=25, decimal_places=22)

    GENERAL = 'General Waste'
    RECYCLING = 'Recycling'
    PLASTIC = 'Plastic'
    PAPER = 'Paper'
    CANS = 'Cans'
    GLASS = 'Glass'

    binTypeChoices = [
        (GENERAL, 'General Waste'),
        (RECYCLING, 'Recycling'),
        (PLASTIC, 'Plastic'),
        (PAPER, 'Paper'),
        (CANS, 'Cans'),
        (GLASS, 'Glass'),
    ]

    binType = models.CharField(
        max_length=25,
        choices=binTypeChoices,
        default=GENERAL
    )


class Product(models.Model):
    barcode = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    details = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products')
    type = models.CharField(max_length=30)
    value = models.IntegerField()


class Transactions(models.Model):
    time = models.DateTimeField("Time occurred", default=time.time())
    bin = models.ForeignKey(BinData, on_delete=models.CASCADE)  # need to assign as foreign key to bin application
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
