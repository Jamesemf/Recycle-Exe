from django.contrib import admin
from .models import Transaction, TransactionLike

# Register your models here.
admin.site.register(Transaction)
admin.site.register(TransactionLike)
