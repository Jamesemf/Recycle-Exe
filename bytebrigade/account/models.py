from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class Statistic(models.Model):
    """
    *** Statistic Model ***

    Data model that record user personal recycle stats.

    Model Fields:
        user: The user object these statistics belong to
        points: The number of points a user object has earned
        carbon: The carbon footprint of a user
        curweek: The points earned in the current week
        curmonth: The points earned in the current month
        curyear: The points earned in the current year
        lastRecycle: The last item that was recycled by a user if there is one
        loveRecycling: The item that an individiuals most likes recycling

    (WARNING: A default product entity with id '1' must be created at initial.)
    """
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
    """
    *** Goal Model ***
    Data model that used to set goal by admin.

    Model Field:
        goalID: The ID of a goal
        name: The name of the goal
        description: A description of the goal
        target: The target they want to achieve in their goal
    """
    goalID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    target = models.DecimalField(max_digits=10, decimal_places=5)


class UserGoal(models.Model):
    """
    *** UserGoal Model ***
    Data model that set by user from Goal entity that set by admin.

    Model Field:
        userGoalID: The ID of the users goal
        userGoalNum: The number of the goal
        user: The user the goal belongs to
        goal: The goal object the user want to achieve
        value: The value of this user goal
        goalType: A String value of goal type about which type of garbage user need to recycle.
    """
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
