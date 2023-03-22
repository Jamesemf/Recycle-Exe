from django.db import models

# Create your models here.


class Product(models.Model):
    """
    *** Product Model ***

    Model Field:
        barcode: the barcode of the product
        name: the name of the product
        weight: the weight of the product
        material: the material of the product
        recycle: if the product can be recycled
        image: an image of the product

    (WARNING: A default product entity with id '1' must be created at initial.)
    """
    barcode = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    weight = models.FloatField()
    material = models.CharField(max_length=100)
    recycle = models.CharField(max_length=30)
    image = models.URLField()

    def __unicode__(self):
        return u'%s' % self.barcode

