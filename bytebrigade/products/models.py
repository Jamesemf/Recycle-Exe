from django.db import models

# Create your models here.


class Product(models.Model):
    """
    *** Product Model ***

    Model Fields:
        barcode:
        name:
        weight:
        material:
        recycle:
        image:
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

