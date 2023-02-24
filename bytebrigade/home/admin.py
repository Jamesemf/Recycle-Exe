from django.contrib import admin

from .models import Transaction, BinData, Product, Statistic
# Register your models here.
admin.site.register(Transaction)
admin.site.register(BinData)
admin.site.register(Product)
admin.site.register(Statistic)
