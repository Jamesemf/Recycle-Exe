from django.db import models

# Create your models here.

class ShopItems(models.Model):
    """
    ***ShopItems Model***

    shop_item_id - the unique id of a product
    shop_item_name - the name of the product
    shop_item_cost - the cost of the product in points
    shop_item_description - a description of the product being sold

    This is a model to contain the information for items that we will sell in the shop page
    Users can spend points on these items. Each item has a QR code associated with it, which we generate ourselvesves.
    """
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    cost = models.IntegerField()
    description = models.CharField(max_length=200)
