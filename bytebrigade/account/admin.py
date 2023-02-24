from django.contrib import admin
from home.models import Transactions, BinData, Product, Statistics
# Register your models here.
admin.site.register(Transactions)
admin.site.register(BinData)
admin.site.register(Product)
admin.site.register(Statistics)
