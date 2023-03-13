from django.db import models
from django.contrib.auth.models import User
import time
# Create your models here.


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


class Product(models.Model):
    barcode = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    weight = models.FloatField()
    material = models.CharField(max_length=100)
    recycle = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % self.barcode


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    bin = models.ForeignKey(BinData, on_delete=models.CASCADE)  # need to assign as foreign key to bin application
    user = models.ForeignKey(User, default=-1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)


class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    carbon = models.FloatField(default=0)
    curweek = models.FloatField(default=0)
    curmonth = models.FloatField(default=0)
    curyear = models.FloatField(default=0)
    lastRecycle = models.ForeignKey(
        Product,
        related_name="lastRecycle",
        on_delete=models.SET_DEFAULT,
        to_field='barcode',
        default='1'
    )
    loveRecycling = models.ForeignKey(
        Product,
        related_name="loveRecycle",
        on_delete=models.SET_DEFAULT,
        to_field='barcode',
        default='1'
    )

    def addToWeek(self, product:dict):
        # as transaction occurs add to 4 cols, points, carbon, cur week, last recycle.
        # add to year and month, but all are reset at the end of a cycle (week, month, year)
        # love = self.calculateLove()
        pass

    def addCurMonth(self, kg):
        # month += last week
        pass

    def addCurYear(self, kg):
        # year += last month
        pass

    def addPoint(self, pts):
        pass

    # goes through transactions and get the product that they recycle the most. This occurs at each recycle event
    def calculateLove(self):
        pass

class Goal(models.Model):
    goalID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    target = models.DecimalField(max_digits=10, decimal_places=5)


class UserGoal(models.Model):
    userGoalID = models.AutoField(primary_key=True)
    userGoalNum = models.IntegerField()
    user = models.ForeignKey(User, default=-1, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, default=-1, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=5)
    
    RECYCLING = 'Recycling'
    PLASTIC = 'Plastic'
    PAPER = 'Paper'
    CANS = 'Cans'
    GLASS = 'Glass'

    goalTypeChoices = [
        (RECYCLING, 'Recycling'),
        (PLASTIC, 'Plastic'),
        (PAPER, 'Paper'),
        (CANS, 'Cans'),
        (GLASS, 'Glass'),
    ]

    goalType = models.CharField(
        max_length=25,
        choices=goalTypeChoices,
        default='Recycling'
    )
