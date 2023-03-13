from django.db import models

# Create your models here.

class Product(models.Model):
    barcode = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    weight = models.FloatField()
    material = models.CharField(max_length=100)
    recycle = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % self.barcode

