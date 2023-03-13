from django.contrib import admin

from .models import Transaction
from bins.models import BinData
from products.models import Product
from account.models import Statistic, UserGoal, Goal

# Register your models here.
admin.site.register(Transaction)
admin.site.register(BinData)
admin.site.register(Product)
admin.site.register(Statistic)
admin.site.register(UserGoal)
admin.site.register(Goal)
