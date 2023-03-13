from django.db import models
from products.models import Product
from django.contrib.auth.models import User



# Create your models here.
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
