from django.db import models
from django.contrib.auth.models import User
from bins.models import BinData
from products.models import Product


class Transaction(models.Model):
    """
    *** Transaction model ***

    This model is used to store data on transactions of users.

    Model Field:
        Transaction_id: The unique id of the transaction
        time: The time the transaction occured (takes the current time)
        bin: The bin object the transaction occured at
        user: The user object that completed the transaction
        product: The product object that was recycled
        likes: A count of the number of likes a transaction recieved

    """
    transaction_id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    bin = models.ForeignKey(BinData, on_delete=models.CASCADE)  # Need to assign as foreign key to bin application
    user = models.ForeignKey(User, default=-1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)


class TransactionLike(models.Model):
    """
    *** TransactionLike model ***

    This model is used to store data on who has liked what transaction

    Model Field:
        Transaction_id: The unique id of the transactionLike
        user: The user object that liked the transaction
        transaction: the transaction object that has been liked

           """
    transactionlike_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)




