from django.db import models
from django.contrib.auth.models import User
from bins.models import BinData
from products.models import Product
import time
# Create your models here.




class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    bin = models.ForeignKey(BinData, on_delete=models.CASCADE)  # need to assign as foreign key to bin application
    user = models.ForeignKey(User, default=-1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)




