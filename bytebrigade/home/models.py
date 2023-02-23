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
    transaction_id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    bin = models.ForeignKey(BinData, on_delete=models.CASCADE)  # need to assign as foreign key to bin application
    user = models.ForeignKey(User, default=-1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)


class Statistics(models.Model):
    user = models.ForeignKey(User, default=-1, on_delete=models.CASCADE)
    points = models.IntegerField()
    carbon = models.DecimalField(max_digits=10, decimal_places=5)
    curweek = models.DecimalField(max_digits=10, decimal_places=5)
    curmonth = models.DecimalField(max_digits=10, decimal_places=5)
    curyear = models.DecimalField(max_digits=10, decimal_places=5)
    lastRecycle = models.ForeignKey(Product, related_name="lastRecycle", default=-1, on_delete=models.CASCADE)
    loveRecycling = models.ForeignKey(Product, related_name="loveRecycle", default=-1, on_delete=models.CASCADE)


class Goals(models.Model):
    goalID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    target = models.DecimalField(max_digits=10, decimal_places=5)


class UserGoals(models.Model):
    userGoalID = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, default=-1, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goals, default=-1, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=5)
