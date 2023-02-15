from django.db import models


class Product(models.Model):
    barcode = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    details = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products')
    type = models.CharField(max_length=30)
    value = models.IntegerField()
