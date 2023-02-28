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
    type = models.CharField(max_length=100)
    weight = models.FloatField()
    category = models.CharField(max_length=100)

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
    carbon = models.DecimalField(default=0, max_digits=10, decimal_places=5)
    curweek = models.DecimalField(default=0, max_digits=10, decimal_places=5)
    curmonth = models.DecimalField(default=0, max_digits=10, decimal_places=5)
    curyear = models.DecimalField(default=0, max_digits=10, decimal_places=5)
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
