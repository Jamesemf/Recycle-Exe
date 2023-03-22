from django.db import models


# Create your models here.

class ShopItems(models.Model):
    """
    ***ShopItems Model***

    Model Field:
        item_id - the unique id of a product
        name - the name of the product
        cost - the cost of the product in points
        description - a description of the product being sold
        stock - the number of this shop items available

    This is a model to contain the information for items that we will sell in the shop page
    Users can spend points on these items. Each item has a QR code associated with it, which we generate ourselvesves.
    """
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default="ticket")
    cost = models.IntegerField(default=0)
    description = models.CharField(max_length=200, default="")
    stock = models.IntegerField(default=1)
